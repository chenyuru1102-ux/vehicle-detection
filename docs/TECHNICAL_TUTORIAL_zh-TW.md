# 從一張影格讀懂整個實驗

## 從像素到標註

YOLO 在一次前向運算中預測影像裡的物件位置、類別與信心分數。Bounding Box 用矩形近似物件範圍。假設圖片寬 800、高 400，車框左上角 (200,100)、右下角 (400,200)，中心是 (300,150)，寬高為 (200,100)。YOLO 標籤將水平量除以圖寬、垂直量除以圖高，因此一行是 `0 0.375 0.375 0.25 0.25`。第一欄是類別編號；一張圖有幾個標註物件就寫幾行。反算後疊回原圖，可以抓出寬高互換、漏框和錯圖配對。

## 道路流程與九支程式

|程式|怎麼用它理解資料流|
|---|---|
|test1.py|早期工具播放影片，按 s 選取當前影格，以 selectROI 圈物件，一併寫入 images 與 labels。|
|extract_frames.py|從 videos 讀 FPS，每隔約兩秒儲存 JPG 到 extracted_frames。跨影片累加編號；檔名本身難以還原來源時間。|
|label_images.py|在擷取影格上反覆選 ROI，轉成類別 0 的正規化框，寫入 new_labels。已有同名標註就跳過。|
|check_label.py|將 new_labels 座標還原成像素並畫綠框，可逐張目視檢查。找不到標註時跳過。|
|split_dataset.py|打亂影格清單（seed 42），依 80/20 分配並複製圖與同名標註。重跑前須檢查目的資料夾是否已有舊檔。|
|check_gpu.py|列印 PyTorch 版本、CUDA 可用性與裝置名稱。歷史執行裝置則查各次 args.yaml。|
|train_yolo.py|現存腳本載入 YOLO11n，指定 CPU、50 epochs、batch 8、640。早期道路實驗使用的模型應讀該次 args.yaml。|
|predict_video.py|讀 train-5 的 best.pt，在夜間影片以 conf 0.25 推論，顯示並儲存結果。|
|predict_video_custom.py|逐幀以 conf 0.20 推論，自行繪製矩形與信心文字，再用原影片尺寸和 FPS 輸出。|

## 停車場流程與九支程式

|程式|怎麼用它理解資料流|
|---|---|
|extract_frames.py|約每秒檢查一次，保留首幀，之後與「上次保留的灰階圖」取像素絕對差的平均值。嚴格大於 15 才存；光照變動也會影響分數。|
|auto_label.py|YOLO11n 以 conf 0.05、尺寸 1280 掃圖，保留 COCO 2、5、7，統一寫成類別 0。以 w 開檔會覆蓋同名人工標籤。|
|label_images.py|讀既有 labels；無標註時以 conf 0.01 預標。左鍵拖曳新增、右鍵刪除點到的框、Z 撤銷最後一框。A 補預標，候選框與現有框 IoU > 0.5 就略過。S 存檔，N/P/Q 也會存。|
|split_dataset.py|從 extracted_frames 與 labels 配對複製到 dataset。先按來源影片分組可降低相鄰影格跨集合的風險。|
|train_combine.py|把 data_combine.yaml 交給 YOLO11n；現存腳本是 CPU、50 epochs、batch 4、416。檔名不足以驗證歷史資料組成。|
|test_parking_video.py|雖名為 video，實際讀取單張驗證圖 parking2_003.jpg，用 train-4/best.pt、conf 0.45、尺寸 416。縮小顯示不會改變推論輸入設定。|
|test_tile.py|取 parking3.mp4 首幀，以寬高一半為界另存四張圖。跨界物件可能被切開。|
|detect_parking.py|對 tile1.jpg 用 YOLO11n、conf 0.05、尺寸 1280，存框圖。全圖座標回填與跨塊去重仍待實作。|
|mark_parking_spaces.py|原檔為零位元組。若要回答哪一格被占用，還需格位幾何、車與格的匹配規則及占用真值。|

## 指標和訓練流程

IoU 是交集面積除以聯集面積。兩個等大面積 100 的框若重疊 60，IoU = 60/(100+100−60) ≈ 0.429。標註工具會留下這個候選框。評估時則用指定 IoU 門檻，把同類預測與真值一對一配對。已被配對的真值即使再被框一次，也不會再算一個 TP。

Precision = TP/(TP+FP)，回答「模型報出的車有多少是真的」。Recall = TP/(TP+FN)，回答「畫面中的車有多少被找到」。假想有十台、報出十二框、其中八框匹配，則 Precision = 8/12，Recall = 8/10。這個算例與歷史資料無關。降低信心門檻可以找回漏車，也可能增加誤報。F1 是兩者的調和平均；F1 curve 可用來觀察門檻取捨。

把預測按信心排序，逐步納入框即可得到 Precision–Recall 曲線；AP 摘要其面積，mAP 再對類別平均。mAP50 採 IoU 0.50，mAP50–95 平均 0.50 至 0.95、間隔 0.05 的十個門檻。嚴格門檻對框位置更敏感。混淆矩陣需先看圖上的預測／真值軸，再用背景列或欄辨認漏檢及誤報。

準備資料時先查圖與同名標籤、可讀性與框位置，再凍結 train/val 名單。訓練將影像分成 batch，模型計算損失並更新權重；走完一輪訓練集是一個 epoch。驗證階段記錄定位、分類損失與偵測指標。比較同一 run 的 train/val 曲線可追蹤學習，但 YOLO26n 的 l1_loss 與 YOLO11n 的 dfl_loss 定義不同。results.png 看歷程，results.csv 查每輪原數，args.yaml 查當次設定。最後一輪數字也不能直接當成 best.pt 的表現。

## 面試時如何說明失敗

道路第一筆最後一輪的 recall 0.8 與 precision 0.00667 可以並存，代表找到不少真值的同時產生大量誤報。單一影格的實際車數無法從整體指標反算。可用同一 run 的 val_batch0_labels.jpg 與 val_batch0_pred.jpg 比較框分布，再查逐框紀錄。若要把改進歸因於模型，需先固定資料切割、標註規則、輸入尺寸與評估程序，再改變單一因素。

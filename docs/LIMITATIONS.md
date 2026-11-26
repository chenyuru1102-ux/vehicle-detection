# Research limitations

1. Randomly splitting frames from the same video may leak near duplicate scenes across training and validation. Independent video or camera splits were not verified.
2. The saved datasets are small: 110 road JPGs and 149 parking JPGs. Their counts may differ from historical training inputs.
3. Road YAML names class 0 `vehicle`; parking YAML names class 0 `car`, while some parking code calls it vehicle. These labels are not semantically identical.
4. Some Python scripts and the private original parking YAML use fixed paths. Reproducing historical runs requires path review.
5. `auto_label.py` opens destination label files with `w`, so rerunning can overwrite manually corrected labels. The interactive tool also writes on save/navigation.
6. No independent test set was confirmed. CSV values are validation values only.
7. Runs used different models and parameters. Comparing their final metrics does not isolate a causal improvement.
8. Only four of ten training directories have CSV results. A folder or plot is not proof of a completed training run.
9. `mark_parking_spaces.py` is empty; occupancy detection is unimplemented. Tiling is exploratory; no full image merge exists.
10. Media provenance, reuse licenses, personal information in frames, and model weight distribution rights remain unverified. Private source files are withheld from the public version.
11. An extreme false positive case of approximately three real vehicles and more than 400 detections is an author recollection only; matching image and count were not verified.

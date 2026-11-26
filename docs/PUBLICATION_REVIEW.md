# Publication review and file lists

## Included in the public archive
- Bilingual READMEs, changelog, limitations, tutorial, V2.0 roadmap, requirements, .gitignore, and portable YAML examples.
- All 18 historical Python files, including empty and early test scripts, plus the road dataset YAML and a redacted parking dataset YAML.
- Ten redacted args.yaml copies, four results.csv files, available PR, F1, P, R, confusion matrix, and results/loss plots.
- Generated comparison.svg, learning_curves.svg, summary.csv, and run inventory.

## Withheld from the public archive; present in the private local archive
- Original videos and rendered videos; source ownership and reuse rights not established.
- Extracted frames, dataset images, labels, parking stills and arbitrary inference JPGs; source rights and identifiable content require review.
- Model weights (*.pt) and zip archives; provenance, distribution rights, and large size require review.
- Virtual environments, IDE files, caches, and each source .git were intentionally excluded from the copied archive because they are environment or repository metadata, not research observations. Original directories retain them.

## Representative cases
- The prototype documented daytime, nighttime and aerial scenes. The V1.0 tree omits the three historical display images.
- Negative: road/train final validation metrics show poor precision/mAP, linked to its YOLO26n args and CSV. Cause not established.
- Recalled extreme overcount: approximately three vehicles and more than 400 detections, **unverified recollection**; no fabricated image or exact count.
- Additional private predictions are inventoried but lack reliable input/model mapping. Their publication and scientific interpretation are deferred.

Public copies of the original execution configurations, with private local paths removed. This applies to the ten run configurations and the parking dataset YAML. The private research archive retains the complete originals. The road dataset YAML already used a relative path.

Gallery provenance: all three images entered Git in 2fff7eb. The archive identifies the scenes, but provides no verified source-frame mapping or redistribution permission. Earlier commits and the v0.1 release archive still expose these images. Their redistribution rights remain unresolved.

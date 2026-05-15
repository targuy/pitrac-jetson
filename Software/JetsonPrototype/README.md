# Jetson Prototype

This package contains the first software seam for an incremental Jetson-based
PiTrac design. It is intentionally hardware-agnostic: the modules define the
interfaces between sensors, camera capture, vision, tracking, calibration, and
output without committing to a specific GPIO, camera, or simulator backend.

The initial goal is a minimal loop:

1. a ball sensor emits a timestamped event;
2. a camera capture component provides frames around that event;
3. a detector reports 2D ball positions;
4. a tracker derives a basic speed/angle estimate;
5. an output publisher exposes the result.

Run the standard-library tests from this directory:

```bash
python -m unittest discover -s tests
```


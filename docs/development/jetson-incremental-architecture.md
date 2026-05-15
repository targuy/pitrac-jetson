---
layout: default
title: Jetson Incremental Architecture
parent: Development Guide
nav_order: 2
description: Incremental Jetson-based PiTrac design that starts with ball sensors and grows toward cameras, 3D tracking, strobes, and simulator output.
keywords: pitrac jetson architecture, jetson golf launch monitor, ball sensors, incremental design
last_modified_date: 2026-05-15
---

# Jetson Incremental Architecture

This document captures the incremental Jetson design direction. The first milestone is deliberately small:
a single Jetson receives ball sensor events, timestamps them reliably, and provides a software seam that can
grow into the full PiTrac launch-monitor pipeline.

## Incremental build path

### 1. Minimal core: Jetson plus ball sensors

- Use one Jetson as the central controller.
- Connect simple ball sensors for presence, impact, or departure detection.
- Produce reliable timestamped events such as `present`, `impact`, and `departure`.
- Do not calculate full trajectory, spin, or 3D reconstruction yet.

### 2. Simple vision prototype

- Add one global-shutter camera.
- Capture frames around the sensor trigger.
- Keep the first image pipeline small: acquisition, 2D ball detection, and debug storage.
- Expected output: ball position in image coordinates for each useful frame.

### 3. Basic speed and angle

- Use multiple frames from the same camera.
- Estimate apparent speed, 2D direction, and a first launch angle.
- Keep calibration simple and explicit.
- Defer spin and 3D reconstruction until the 2D path is stable.

### 4. Second camera and 3D geometry

- Add a synchronized second camera.
- Introduce stereo calibration.
- Estimate an initial 3D trajectory.
- Keep acquisition, detection, reconstruction, and publishing separated.

### 5. Lighting and strobe control

- Add Jetson GPIO or a replaceable GPIO adapter for strobe control.
- Synchronize sensors, cameras, and lighting.
- Keep the strobe module replaceable because the hardware may change.

### 6. Web-first operation

- Start with system state, logs, and the last shot estimate.
- Add calibration, hardware configuration, and sensor/camera tests after the core loop is stable.
- Reuse PiTrac's web-first approach rather than requiring manual configuration file edits.

### 7. Simulator output

- Publish stable shot estimates through a simulator-neutral output interface.
- Add GSPro, E6, or other simulator adapters after the measurement pipeline is reliable.

### 8. Physical integration

- Begin with a wired prototype.
- Move to a Jetson-specific enclosure once sensor, camera, and strobe positions are known.
- Design an interface board only after the wiring has stabilized.
- Leave room for additional cameras or more advanced sensors.

## Software seams

The prototype package at `Software/JetsonPrototype/` defines the first module boundaries:

| Module | Responsibility |
| --- | --- |
| `sensors` | Timestamped ball events from presence, impact, or departure sensors |
| `capture` | Camera frames captured around a trigger event |
| `vision` | 2D ball detections in captured frames |
| `tracking` | Basic speed and angle estimates, later 3D trajectory |
| `calibration` | Calibration values used by tracking stages |
| `output` | Publishing to web UI, APIs, message brokers, or simulator adapters |
| `pipeline` | Minimal orchestration between the modules |

The first implementation uses deterministic, hardware-free components so the interfaces can be tested before
Jetson-specific GPIO and camera libraries are selected.

## Near-term implementation tasks

1. Select the initial Jetson model and sensor wiring assumptions.
2. Add a real sensor backend behind the `sensors` interface.
3. Add a Jetson camera backend behind the `capture` interface.
4. Replace scripted detection with a first global-shutter image detector.
5. Surface pipeline status and the last shot estimate in the web UI.
6. Add strobe control once capture timing is measurable.
7. Expand tracking from 2D estimates to synchronized two-camera geometry.


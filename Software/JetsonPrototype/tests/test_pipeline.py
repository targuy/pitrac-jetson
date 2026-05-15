import unittest

from pitrac_jetson import (
    BallEvent,
    BallEventType,
    BallPosition,
    Basic2DTracker,
    CalibrationProfile,
    CameraFrame,
    DetectionSample,
    JetsonPrototypePipeline,
    MemoryShotPublisher,
    ScriptedBallDetector,
    ScriptedBallSensor,
    SyntheticFrameCapture,
)


class JetsonPrototypePipelineTest(unittest.TestCase):
    def test_pipeline_publishes_basic_2d_track(self) -> None:
        sensor = ScriptedBallSensor(
            [BallEvent(timestamp_ns=1_000_000_000, event_type=BallEventType.DEPARTURE, sensor_id="beam-1")]
        )
        capture = SyntheticFrameCapture(
            [
                CameraFrame(camera_id="cam-1", timestamp_ns=1_000_000_000, width=640, height=480),
                CameraFrame(camera_id="cam-1", timestamp_ns=1_100_000_000, width=640, height=480),
            ]
        )
        detector = ScriptedBallDetector(
            [
                DetectionSample("cam-1", 1_000_000_000, BallPosition(10.0, 10.0)),
                DetectionSample("cam-1", 1_100_000_000, BallPosition(110.0, 10.0)),
            ]
        )
        publisher = MemoryShotPublisher()

        estimate = JetsonPrototypePipeline(
            sensor=sensor,
            capture=capture,
            detector=detector,
            tracker=Basic2DTracker(),
            calibration=CalibrationProfile(name="test", pixels_per_meter=100.0),
            publisher=publisher,
        ).run_once()

        self.assertIsNotNone(estimate)
        self.assertAlmostEqual(10.0, estimate.speed_mps)
        self.assertAlmostEqual(0.0, estimate.angle_deg)
        self.assertEqual([estimate], publisher.estimates)

    def test_pipeline_returns_none_without_two_detections(self) -> None:
        publisher = MemoryShotPublisher()

        estimate = JetsonPrototypePipeline(
            sensor=ScriptedBallSensor(
                [BallEvent(timestamp_ns=1, event_type=BallEventType.PRESENT, sensor_id="presence")]
            ),
            capture=SyntheticFrameCapture([CameraFrame("cam-1", 1, 640, 480)]),
            detector=ScriptedBallDetector([DetectionSample("cam-1", 1, BallPosition(10.0, 10.0))]),
            tracker=Basic2DTracker(),
            calibration=CalibrationProfile(),
            publisher=publisher,
        ).run_once()

        self.assertIsNone(estimate)
        self.assertEqual([], publisher.estimates)


if __name__ == "__main__":
    unittest.main()


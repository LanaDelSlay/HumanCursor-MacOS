from time import sleep
import random
import pyautogui
from Quartz.CoreGraphics import CGEventCreateMouseEvent, kCGEventMouseMoved, kCGMouseButtonLeft, CGEventPost, kCGHIDEventTap
import AppKit

from humancursor.utilities.human_curve_generator import HumanizeMouseTrajectory
from humancursor.utilities.calculate_and_randomize import generate_random_curve_parameters


class SystemCursor:

    @staticmethod
    def move_to(point: list or tuple, duration: int or float = None, human_curve=None, steady=False):
        """Moves to certain coordinates of screen"""
        from_point = AppKit.NSEvent.mouseLocation()

        if not human_curve:
            (
                offset_boundary_x,
                offset_boundary_y,
                knots_count,
                distortion_mean,
                distortion_st_dev,
                distortion_frequency,
                tween,
                target_points,
            ) = generate_random_curve_parameters(
                pyautogui, from_point, point
            )
            if steady:
                offset_boundary_x, offset_boundary_y = 10, 10
                distortion_mean, distortion_st_dev, distortion_frequency = 1.2, 1.2, 1
            human_curve = HumanizeMouseTrajectory(
                from_point,
                point,
                offset_boundary_x=offset_boundary_x,
                offset_boundary_y=offset_boundary_y,
                knots_count=knots_count,
                distortion_mean=distortion_mean,
                distortion_st_dev=distortion_st_dev,
                distortion_frequency=distortion_frequency,
                tween=tween,
                target_points=target_points,
            )

        if duration is None:
            duration = random.uniform(0.5, 2.0)
        delay = duration / len(human_curve.points)
        for pnt in human_curve.points:
            event = CGEventCreateMouseEvent(None, kCGEventMouseMoved, (pnt[0], pnt[1]), kCGMouseButtonLeft)
            CGEventPost(kCGHIDEventTap, event)
            sleep(delay)
        CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventMouseMoved, (point[0], point[1]), kCGMouseButtonLeft))

    def click_on(self, point: list or tuple, clicks: int = 1, click_duration: int or float = 0, steady=False):
        """Clicks a specified number of times, on the specified coordinates"""
        self.move_to(point, steady=steady)
        for _ in range(clicks):
            self.mouse_down()
            sleep(click_duration)
            self.mouse_down()
            sleep(random.uniform(0.170, 0.280))

    def drag_and_drop(self, from_point: list or tuple, to_point: list or tuple, duration: int or float or [float, float] or (float, float) = None, steady=False):
        """Drags from a certain point, and releases to another"""
        if isinstance(duration, (list, tuple)):
            first_duration, second_duration = duration
        elif isinstance(duration, (float, int)):
            first_duration = second_duration = duration / 2
        else:
            first_duration = second_duration = None

        self.move_to(from_point, duration=first_duration)
        self.mouse_down()
        self.move_to(to_point, duration=second_duration, steady=steady)
        self.mouse_down()

    def mouse_down():
        current_location = AppKit.NSEvent.mouseLocation()
        screen_height = AppKit.NSScreen.mainScreen().frame().size.height
        corrected_y = screen_height - current_location.y
        event = CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (current_location.x, corrected_y), kCGMouseButtonLeft)
        CGEventPost(kCGHIDEventTap, event)

    def mouse_up():
        current_location = AppKit.NSEvent.mouseLocation()
        screen_height = AppKit.NSScreen.mainScreen().frame().size.height
        corrected_y = screen_height - current_location.y
        event = CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (current_location.x, corrected_y), kCGMouseButtonLeft)
        CGEventPost(kCGHIDEventTap, event)
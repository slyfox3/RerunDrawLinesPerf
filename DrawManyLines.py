import time

import click
import rerun as rr

from rerun.datatypes import RotationAxisAngle


def one_strip(number_points: int):
    return rr.LineStrips3D(
        [[0.3 if i % 2 == 0 else -0.3, i, 0] for i in range(number_points)],
    )


def rotate(theta: float):
    return rr.Transform3D(
        rotation_axis_angle=RotationAxisAngle(axis=[0, 0, 1], degrees=theta),
        axis_length=0,
    )


def draw_lines(lines_count: int, pts_per_line: int):
    theta_delta = 360 / lines_count
    zig_zag = one_strip(pts_per_line)
    for i in range(lines_count):
        rr.log(
            f"line_{i}",
            rotate(theta_delta * i),
            static=True,
        )
        rr.log(
            f"line_{i}/strip",
            zig_zag,
            static=True,
        )


@click.command()
@click.option(
    "--count",
    type=int,
    default=500,
    help="Number of lines to draw",
)
@click.option(
    "--pts-per-line",
    type=int,
    default=10,
    help="Number of points per line strip",
)
@click.option(
    "--ws-port",
    type=int,
    default=-1,
    help="Port number to serve websocket",
)
def main(ws_port: int, count: int, pts_per_line: int):
    # Prep Rerun
    rr.init("Many Lines", spawn=ws_port < 0)
    if ws_port > 0:
        rr.serve(
            open_browser=False,
            ws_port=ws_port,
        )
    else:
        rr.connect()

    # Now, render
    draw_lines(count, pts_per_line)

    print("Done drawing lines.")
    print("Press Ctrl+C to exit.")
    while True:
        time.sleep(0.5)


if __name__ == "__main__":
    main()

import pygame
import random
import math
from pygame.locals import QUIT


def mark_pixel(surface: pygame.Surface, pos: tuple[int, int], plane: int) -> None:
    """
    Change the color of a pixel at a given position on the surface.
    Args:
        surface: Surface to draw on.
        pos: Position of the pixel.
        plane: Color plane to modify.
    """
    col = surface.get_at(pos)
    v = min(col[plane] + 4, 255)
    new_color = [v if i == plane else col[i] for i in range(3)]
    surface.set_at(pos, new_color)


def random_point_index(polygon_length: int) -> int:
    """
    Select a random index from the polygon's vertices.
    Ensure the selected index doesn't create a degenerate triangle.
    Args:
        polygon_length: Number of vertices in the polygon.
    Returns:
        Random index for the polygon's vertices.
    """
    if polygon_length <= 3:
        return random.randint(0, polygon_length - 1)

    idx = random.sample(range(polygon_length), 3)
    idx.sort()
    dst1 = abs(idx[1] - idx[2])

    while True:
        idx[0] = random.randint(0, polygon_length - 1)
        dst = abs(idx[0] - idx[1])
        if dst1 == 0 and (dst == 1 or dst == polygon_length - 1):
            continue
        else:
            break

    return idx[0]


def init_polygon(width: int, height: int, n: int) -> list[tuple[float, float]]:
    """
    Initialize the vertices of a regular polygon.
    Args:
        width: Width of the surface.
        height: Height of the surface.
        n: Number of sides of the polygon.
    Returns:
        List of vertices for the polygon.
    """
    delta_angle = 360 / n
    r = width / 2 - 10
    polygon = []

    for i in range(n):
        angle = (180 + i * delta_angle) * math.pi / 180
        polygon.append((width / 2 + r * math.sin(angle),
                        height / 2 + r * math.cos(angle)))
    return polygon


def calculate_optimal_ratio(n: int) -> float:
    """
    Calculate the optimal ratio for the chaos game.

    The optimal ratio is calculated using the formula:

    r_opt = (1 + 2a) / (2 + 2a)

    where:
    - 'a' is the sum of cosines, calculated as Σ_{i=1}^{n/4} cos(i(π - θ))
    - Σ represents the sum from i=1 to n/4
    - θ is the internal angle of the polygon, calculated as (n - 2)π/n
    - n is the number of sides of the polygon

    Args:
        n: Number of sides of the polygon.

    Returns:
        Optimal ratio.
    """
    if n <= 2:
        raise ValueError("Number of sides must be greater than 2.")

    theta = (n - 2) * math.pi / n
    n_protruding = n // 4

    a = sum([math.cos(i * (math.pi - theta))
             for i in range(1, n_protruding + 1)])
    r_opt = (1 + 2 * a) / (2 + 2 * a)
    return r_opt


def main(width: int, height: int, n: int, r: float) -> None:
    """
    Main function to run the chaos game simulation.
    Args:
        width: Width of the surface.
        height: Height of the surface.
        n: Number of sides of the polygon.
        r: Ratio for the movement of points.
    """
    pygame.init()
    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Chaos Simulation')

    polygon = init_polygon(width, height, n)
    x = [float(random.randint(0, width)) for _ in range(3)]
    y = [float(random.randint(0, height)) for _ in range(3)]
    plane_randomness = [0.02, 0.04, 0.08]

    step = 0
    while True:
        step += 1
        i = random_point_index(n)

        for plane_idx in range(3):
            rr = random.random() * plane_randomness[plane_idx]
            x[plane_idx] += (polygon[i][0] - x[plane_idx]) * (r + rr)
            y[plane_idx] += (polygon[i][1] - y[plane_idx]) * (r + rr)

            if 0 <= x[plane_idx] <= width and 0 <= y[plane_idx] <= height:
                mark_pixel(
                    surface, (int(x[plane_idx]), int(y[plane_idx])), plane_idx)

        if step % 5000 == 0:
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.image.save(surface, 'simulation.jpg')
                pygame.quit()
                return


if __name__ == "__main__":
    n = int(input("Enter the number of sides of the polygon: "))
    r_input = input("Enter the ratio ('optimal' for optimal ratio): ")

    if r_input == 'optimal':
        r = calculate_optimal_ratio(n)
    else:
        r = float(r_input)

    print(f"Starting chaos simulation - sides: {n}, ratio: {r}.")
    main(800, 800, n, r)

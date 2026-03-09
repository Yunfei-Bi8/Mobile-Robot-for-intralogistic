import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

class MAP:
    def __init__(self, size=10):
        self.size = size
        self.grid = np.zeros((size, size))  # initialize grid with zeros (unknown)
        self.robot_position = None
        self.marker_positions = {}
        self.walls = [[(0,0),(5,0)],[(0,0),(0,10)],[(5,0),(5,5)],[(5,5),(10,5)],[(10,5),(10,10)],[(0,10),(10,10)]]

    def add_marker(self, marker_id, x, y):
        self.marker_positions[marker_id] = (x, y)

    def show_map(self):
        self._draw_map()
        plt.show()

    def save_map(self, filename="map_output.png"):
        """save the map as an image file"""
        self._draw_map()
        plt.savefig(filename)
        plt.close()
        print(f"map saved as {filename}")

    def auto_save_map(self, snapshot_id):
        filename = f"map_{snapshot_id:03d}.png"
        self.save_map(filename)



    def _draw_map(self):
        """use matplotlib to draw the map with walls, markers and robot position"""
        plt.figure(figsize=(6, 6))
        plt.xlim(-2, self.size + 2)
        plt.ylim(-2, self.size + 2)
        plt.grid(True)
        plt.gca().set_aspect('equal')
        
        for (x1,y1), (x2,y2) in self.walls:
            plt.plot([x1,x2],[y1,y2], '-k', linewidth=2)

        for marker_id, (x, y) in self.marker_positions.items():
            square_size = 1
            
            square = Rectangle((x-square_size/2, y-square_size/2), square_size, square_size, facecolor='blue', edgecolor='blue')
            plt.gca().add_patch(square)
            
            plt.plot(x, y, 'bo')
            plt.text(x, y + 2, f"ID {marker_id}", fontsize=8)

        if self.robot_position:
            x, y = self.robot_position
            
            triangle_size = 1
            triangle = Polygon([(x, y+triangle_size/2), (x-triangle_size/2, y-triangle_size/2), (x+triangle_size/2, y - triangle_size/2)],closed = True, facecolor = 'red', edgecolor = 'red')
            
            plt.gca().add_patch(triangle)
            plt.text(x , y + 2, "Robot", color='red')

        plt.title("Robot Map (dm)")
        plt.xlabel("X (dm)")
        plt.ylabel("Y (dm)")

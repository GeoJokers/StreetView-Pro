from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from qgis.PyQt.QtCore import Qt, QPointF, QTimer
from qgis.PyQt.QtWidgets import QAction, QToolBar, QApplication, QMenu
from qgis.PyQt.QtGui import QIcon, QColor, QCursor, QPixmap

import os.path
import math
import webbrowser


class StreetViewPro:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.tool = None
        self.toolbar = None
        self.context_menu_actions = []
        self.qgis_version = Qgis.QGIS_VERSION_INT

    def initGui(self):
        self.toolbar = self.iface.addToolBar("StreetView Pro Toolbar")
        self.toolbar.setObjectName("StreetViewProToolbar")
        
        icon_path = os.path.join(self.plugin_dir, 'streetviewpro.png')
        self.action = QAction(
            QIcon(icon_path), 
            "Open StreetView Pro", 
            self.iface.mainWindow()
        )
        self.action.setCheckable(True)
        self.action.triggered.connect(self.run)
        self.action.setToolTip("Click or drag on map to open Street View")
        
        self.toolbar.addAction(self.action)
        self.iface.addPluginToMenu("&StreetView Pro", self.action)
        
        self.setup_context_menu()
        
    def setup_context_menu(self):
        """Setup right-click context menu options compatible with all QGIS versions"""
        canvas = self.iface.mapCanvas()
        
        if self.qgis_version < 33000:
            canvas.setContextMenuPolicy(Qt.CustomContextMenu)
            canvas.customContextMenuRequested.connect(self.show_context_menu_modern)
        else:
            try:
                canvas.contextMenuAboutToShow.connect(self.add_context_menu_items)
            except AttributeError:
                canvas.setContextMenuPolicy(Qt.CustomContextMenu)
                canvas.customContextMenuRequested.connect(self.show_context_menu_modern)
        
    def add_context_menu_items(self, menu, event):
        """Original context menu method for QGIS 3.34+"""
        point = self.iface.mapCanvas().getCoordinateTransform().toMapCoordinates(event.pos())
        
        action1 = QAction("Open Street View Here", menu)
        action1.triggered.connect(lambda: self.open_streetview_at_point(point))
        
        action2 = QAction("Copy Coordinate", menu)
        action2.triggered.connect(lambda: self.copy_coordinate(point))
        
        action3 = QAction("Copy Street View URL", menu)
        action3.triggered.connect(lambda: self.copy_streetview_url(point))
        
        menu.addAction(action1)
        menu.addAction(action2)
        menu.addAction(action3)
        
    def show_context_menu_modern(self, point):
        """Modern context menu method for QGIS 3.10"""
        menu = QMenu()
        
        map_point = self.iface.mapCanvas().getCoordinateTransform().toMapCoordinates(point)
        
        action1 = QAction("Open Street View Here", menu)
        action1.triggered.connect(lambda: self.open_streetview_at_point(map_point))
        
        action2 = QAction("Copy Coordinate", menu)
        action2.triggered.connect(lambda: self.copy_coordinate(map_point))
        
        action3 = QAction("Copy Street View URL", menu)
        action3.triggered.connect(lambda: self.copy_streetview_url(map_point))
        
        menu.addAction(action1)
        menu.addAction(action2)
        menu.addAction(action3)
        
        global_point = self.iface.mapCanvas().mapToGlobal(point)
        menu.exec_(global_point)
        
    def open_streetview_at_point(self, point):
        """Open Street View at the given point with default heading"""
        try:
            actual_crs = self.iface.mapCanvas().mapSettings().destinationCrs()
            crsDest = QgsCoordinateReferenceSystem(4326)
            xform = QgsCoordinateTransform(actual_crs, crsDest, QgsProject.instance())
            pt_wgs84 = xform.transform(point)
            
            heading = 0
            
            url = f'https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={pt_wgs84.y()},{pt_wgs84.x()}&heading={heading}&pitch=10&fov=250'
            webbrowser.open_new(url)
            
        except Exception as e:
            self.iface.messageBar().pushMessage(
                "Error",
                f"Failed to open Street View: {str(e)}",
                level=Qgis.Critical,
                duration=5
            )
    
    def copy_coordinate(self, point):
        """Copy coordinate to clipboard in project CRS"""
        try:
            coord_text = f"{point.x():.1f}, {point.y():.1f}"
            
            clipboard = QApplication.clipboard()
            clipboard.setText(coord_text)
            
            self.iface.messageBar().pushMessage(
                "StreetView Pro",
                f"Coordinate copied: {coord_text}",
                level=Qgis.Success,
                duration=3
            )
            
        except Exception as e:
            self.iface.messageBar().pushMessage(
                "Error",
                f"Failed to copy coordinate: {str(e)}",
                level=Qgis.Critical,
                duration=5
            )
    
    def copy_streetview_url(self, point):
        """Copy Street View URL to clipboard"""
        try:
            actual_crs = self.iface.mapCanvas().mapSettings().destinationCrs()
            crsDest = QgsCoordinateReferenceSystem(4326)
            xform = QgsCoordinateTransform(actual_crs, crsDest, QgsProject.instance())
            pt_wgs84 = xform.transform(point)
            
            heading = 0
            
            url = f'https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={pt_wgs84.y()},{pt_wgs84.x()}&heading={heading}&pitch=10&fov=250'
            
            clipboard = QApplication.clipboard()
            clipboard.setText(url)
            
            self.iface.messageBar().pushMessage(
                "StreetView Pro",
                "Street View URL copied to clipboard",
                level=Qgis.Success,
                duration=3
            )
            
        except Exception as e:
            self.iface.messageBar().pushMessage(
                "Error",
                f"Failed to copy URL: {str(e)}",
                level=Qgis.Critical,
                duration=5
            )
        
    def unload(self):
        if self.toolbar:
            self.toolbar.deleteLater()
            self.toolbar = None
        
        self.iface.removePluginMenu("&StreetView Pro", self.action)
        
        if self.tool:
            self.iface.mapCanvas().unsetMapTool(self.tool)
            self.tool = None

    def run(self):
        self.iface.messageBar().pushMessage(
            "StreetView Pro", 
            "Click or drag the cursor to open the Street View",
            level=Qgis.Info,
            duration=5
        )
        
        if not self.tool:
            self.tool = PointTool(self.iface.mapCanvas(), self.iface, self.action, self.plugin_dir)
        
        self.iface.mapCanvas().setMapTool(self.tool)
        self.action.setChecked(True)


class PointTool(QgsMapTool):

    def __init__(self, canvas, iface, action, plugin_dir):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.iface = iface
        self.action = action
        self.plugin_dir = plugin_dir
        
        self.pressed = False
        self.line_active = False
        self.point0 = None
        self.point1 = None
        self.rb = None
        self.rl = None
        self.arrow = None
        
        # Load 11 cursor icons
        self.cursor_left5 = self.load_cursor('left5.png')
        self.cursor_left4 = self.load_cursor('left4.png')
        self.cursor_left3 = self.load_cursor('left3.png')
        self.cursor_left2 = self.load_cursor('left2.png')
        self.cursor_left1 = self.load_cursor('left1.png')
        self.cursor_center = self.load_cursor('center.png')
        self.cursor_right1 = self.load_cursor('right1.png')
        self.cursor_right2 = self.load_cursor('right2.png')
        self.cursor_right3 = self.load_cursor('right3.png')
        self.cursor_right4 = self.load_cursor('right4.png')
        self.cursor_right5 = self.load_cursor('right5.png')
        
        # Current cursor state
        self.current_cursor = self.cursor_center
        
        # Track cursor movement for velocity calculation
        self.last_pos = None
        self.last_time = None
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Animation timer for cursor updates
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_cursor)
        self.animation_timer.start(50)  # Update every 50ms
        
    def load_cursor(self, filename):
        """Load a cursor icon from file"""
        cursor_path = os.path.join(self.plugin_dir, filename)
        if os.path.exists(cursor_path):
            cursor_pixmap = QPixmap(cursor_path)
            
            # Scale the cursor to desired size
            desired_size = 52  # Change this value to control size (in pixels)
            cursor_pixmap = cursor_pixmap.scaled(
                desired_size, 
                desired_size, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            
            # Set hotspot at top-center for hanging effect
            hotspot_x = cursor_pixmap.width() // 2
            hotspot_y = 0
            return QCursor(cursor_pixmap, hotspot_x, hotspot_y)
        else:
            # Fallback to cross cursor
            return QCursor(Qt.CrossCursor)
    
    def calculate_velocity(self, current_pos):
        """Calculate cursor velocity"""
        from qgis.PyQt.QtCore import QDateTime
        
        current_time = QDateTime.currentMSecsSinceEpoch()
        
        if self.last_pos is not None and self.last_time is not None:
            time_diff = (current_time - self.last_time) / 1000.0
            
            if time_diff > 0:
                dx = current_pos.x() - self.last_pos.x()
                dy = current_pos.y() - self.last_pos.y()
                
                # Calculate velocity
                self.velocity_x = dx / time_diff
                self.velocity_y = dy / time_diff
        
        self.last_pos = current_pos
        self.last_time = current_time
    
    def update_cursor(self):
        """Update cursor based on movement direction and speed"""
        # Speed thresholds (pixels per second)
        # Adjust these values to change sensitivity:
        threshold_stationary = 5.0    # Below this = stationary (center icon)
        threshold_level1 = 20.0        # Slow movement (left1/right1)
        threshold_level2 = 50.0        # Medium-slow (left2/right2)
        threshold_level3 = 100.0       # Medium (left3/right3)
        threshold_level4 = 200.0       # Fast (left4/right4)
        # Above threshold_level4 = very fast (left5/right5)
        
        abs_velocity_x = abs(self.velocity_x)
        
        # Determine which cursor to show based on horizontal velocity
        new_cursor = None
        
        if abs_velocity_x < threshold_stationary:
            # Stationary or very slow - show center
            new_cursor = self.cursor_center
        else:
            # Moving horizontally (or diagonally with horizontal component)
            if self.velocity_x > 0:
                # Moving RIGHT - show LEFT icons (momentum effect)
                if abs_velocity_x < threshold_level1:
                    new_cursor = self.cursor_left1
                elif abs_velocity_x < threshold_level2:
                    new_cursor = self.cursor_left2
                elif abs_velocity_x < threshold_level3:
                    new_cursor = self.cursor_left3
                elif abs_velocity_x < threshold_level4:
                    new_cursor = self.cursor_left4
                else:
                    new_cursor = self.cursor_left5
            else:
                # Moving LEFT - show RIGHT icons (momentum effect)
                if abs_velocity_x < threshold_level1:
                    new_cursor = self.cursor_right1
                elif abs_velocity_x < threshold_level2:
                    new_cursor = self.cursor_right2
                elif abs_velocity_x < threshold_level3:
                    new_cursor = self.cursor_right3
                elif abs_velocity_x < threshold_level4:
                    new_cursor = self.cursor_right4
                else:
                    new_cursor = self.cursor_right5
        
        # Update cursor if changed
        if new_cursor != self.current_cursor:
            self.current_cursor = new_cursor
            self.canvas.setCursor(self.current_cursor)

    def canvasPressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        
        # Handle right-click separately
        if event.button() == Qt.RightButton:
            self.show_context_menu(event.pos())
            return
        
        # Left-click behavior
        if not self.pressed:
            self.pressed = True
            self.rb = QgsRubberBand(self.canvas, QgsWkbTypes.GeometryType.PointGeometry)
            self.rb.setColor(QColor("#fdbf2d"))
            self.rb.setWidth(3)
            self.point0 = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
            self.rb.addPoint(self.point0)
    
    def show_context_menu(self, pos):
        """Show context menu on right-click"""
        menu = QMenu()
        
        # Get map point from screen position
        map_point = self.canvas.getCoordinateTransform().toMapCoordinates(pos)
        
        action1 = QAction("Open Street View Here", menu)
        action1.triggered.connect(lambda: self.open_streetview_at_point(map_point))
        
        action2 = QAction("Copy Coordinate", menu)
        action2.triggered.connect(lambda: self.copy_coordinate(map_point))
        
        action3 = QAction("Copy Street View URL", menu)
        action3.triggered.connect(lambda: self.copy_streetview_url(map_point))
        
        menu.addAction(action1)
        menu.addAction(action2)
        menu.addAction(action3)
        
        # Show menu at cursor position
        global_point = self.canvas.mapToGlobal(pos)
        menu.exec_(global_point)
    
    def open_streetview_at_point(self, point):
        """Open Street View at the given point with default heading"""
        try:
            actual_crs = self.canvas.mapSettings().destinationCrs()
            crsDest = QgsCoordinateReferenceSystem(4326)
            xform = QgsCoordinateTransform(actual_crs, crsDest, QgsProject.instance())
            pt_wgs84 = xform.transform(point)
            
            heading = 0
            
            url = f'https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={pt_wgs84.y()},{pt_wgs84.x()}&heading={heading}&pitch=10&fov=250'
            webbrowser.open_new(url)
            
        except Exception as e:
            self.iface.messageBar().pushMessage(
                "Error",
                f"Failed to open Street View: {str(e)}",
                level=Qgis.Critical,
                duration=5
            )
    
    def copy_coordinate(self, point):
        """Copy coordinate to clipboard in project CRS"""
        try:
            coord_text = f"{point.x():.1f}, {point.y():.1f}"
            
            clipboard = QApplication.clipboard()
            clipboard.setText(coord_text)
            
            self.iface.messageBar().pushMessage(
                "StreetView Pro",
                f"Coordinate copied: {coord_text}",
                level=Qgis.Success,
                duration=3
            )
            
        except Exception as e:
            self.iface.messageBar().pushMessage(
                "Error",
                f"Failed to copy coordinate: {str(e)}",
                level=Qgis.Critical,
                duration=5
            )
    
    def copy_streetview_url(self, point):
        """Copy Street View URL to clipboard"""
        try:
            actual_crs = self.canvas.mapSettings().destinationCrs()
            crsDest = QgsCoordinateReferenceSystem(4326)
            xform = QgsCoordinateTransform(actual_crs, crsDest, QgsProject.instance())
            pt_wgs84 = xform.transform(point)
            
            heading = 0
            
            url = f'https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={pt_wgs84.y()},{pt_wgs84.x()}&heading={heading}&pitch=10&fov=250'
            
            clipboard = QApplication.clipboard()
            clipboard.setText(url)
            
            self.iface.messageBar().pushMessage(
                "StreetView Pro",
                "Street View URL copied to clipboard",
                level=Qgis.Success,
                duration=3
            )
            
        except Exception as e:
            self.iface.messageBar().pushMessage(
                "Error",
                f"Failed to copy URL: {str(e)}",
                level=Qgis.Critical,
                duration=5
            )

    def canvasMoveEvent(self, event):
        # Update velocity calculation
        self.calculate_velocity(event.pos())
        
        x = event.pos().x()
        y = event.pos().y()
        
        if self.pressed:
            self.point1 = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
            
            if not self.line_active:
                self.rl = QgsRubberBand(self.canvas, QgsWkbTypes.GeometryType.LineGeometry)
                self.rl.setColor(QColor("#fdbf2d"))
                self.rl.setWidth(2)
                self.rl.addPoint(self.point0)
                self.rl.addPoint(self.point1)
                self.line_active = True
            else:
                self.rl.reset(QgsWkbTypes.LineGeometry)
                self.rl.setColor(QColor("#fdbf2d"))
                self.rl.setWidth(2)
                self.rl.addPoint(self.point0)
                self.rl.addPoint(self.point1)
            
            self.draw_arrow()

    def draw_arrow(self):
        """Draw an arrow head at the end of the line"""
        if self.arrow:
            self.arrow.reset(QgsWkbTypes.LineGeometry)
        else:
            self.arrow = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
            self.arrow.setColor(QColor("#fdbf2d"))
            self.arrow.setWidth(2)
        
        if self.point0 and self.point1:
            angle = math.atan2(self.point1.y() - self.point0.y(), self.point1.x() - self.point0.x())
            
            arrow_length = 20
            arrow_width = 10
            
            map_units_per_pixel = self.canvas.mapUnitsPerPixel()
            arrow_length_map = arrow_length * map_units_per_pixel
            arrow_width_map = arrow_width * map_units_per_pixel
            
            left_angle = angle + math.radians(150)
            left_x = self.point1.x() + arrow_length_map * math.cos(left_angle)
            left_y = self.point1.y() + arrow_length_map * math.sin(left_angle)
            left_point = QgsPointXY(left_x, left_y)
            
            right_angle = angle - math.radians(150)
            right_x = self.point1.x() + arrow_length_map * math.cos(right_angle)
            right_y = self.point1.y() + arrow_length_map * math.sin(right_angle)
            right_point = QgsPointXY(right_x, right_y)
            
            self.arrow.addPoint(left_point)
            self.arrow.addPoint(self.point1)
            self.arrow.addPoint(right_point)

    def canvasReleaseEvent(self, event):
        if not self.pressed:
            return
        
        if self.point1 is None:
            x = event.pos().x()
            y = event.pos().y()
            self.point1 = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
            
        try:
            angle = math.atan2(self.point1.x() - self.point0.x(), self.point1.y() - self.point0.y())
            angle = math.degrees(angle) if angle > 0 else (math.degrees(angle) + 180) + 180
            
            actual_crs = self.canvas.mapSettings().destinationCrs()
            crsDest = QgsCoordinateReferenceSystem(4326)
            xform = QgsCoordinateTransform(actual_crs, crsDest, QgsProject.instance())
            pt1 = xform.transform(self.point0)
            
            url = f'https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={pt1.y()},{pt1.x()}&heading={int(angle)}&pitch=10&fov=250'
            webbrowser.open_new(url)
            
        except Exception as e:
            self.iface.messageBar().pushMessage(
                "Error",
                f"Failed to open Street View: {str(e)}",
                level=Qgis.Critical,
                duration=5
            )
        
        finally:
            self.cleanup()
            self.action.setChecked(False)
            self.canvas.unsetMapTool(self)
            self.iface.actionSelect().trigger()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.cleanup()
            self.action.setChecked(False)
            self.canvas.unsetMapTool(self)
            self.iface.actionSelect().trigger()

    def cleanup(self):
        if self.rl:
            self.rl.reset()
            self.rl = None
        if self.rb:
            self.rb.reset()
            self.rb = None
        if self.arrow:
            self.arrow.reset()
            self.arrow = None
        
        self.pressed = False
        self.line_active = False
        self.point0 = None
        self.point1 = None
        
        # Reset velocity
        self.velocity_x = 0
        self.velocity_y = 0
        self.last_pos = None
        self.last_time = None

    def activate(self):
        # Reset all tracking variables
        self.last_pos = None
        self.last_time = None
        self.velocity_x = 0
        self.velocity_y = 0
        self.current_cursor = self.cursor_center
        
        # Restart the animation timer
        if not self.animation_timer.isActive():
            self.animation_timer.start(50)
        
        self.canvas.setCursor(self.cursor_center)

    def deactivate(self):
        self.cleanup()
        self.action.setChecked(False)
        if self.animation_timer:
            self.animation_timer.stop()

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True
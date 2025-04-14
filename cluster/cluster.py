import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer, QRectF

# Initialize QApplication at the top
app = QApplication(sys.argv)
screen_geometry = app.primaryScreen().geometry()
width = screen_geometry.width()
height = screen_geometry.height()
gauge_size = int(250 * width / 800)

class SpeedProgress(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = 0
        self.setFixedSize(gauge_size, gauge_size)

    def setValue(self, value):
        self.value = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(5 * width / 800, 5 * width / 800, gauge_size - 10 * width / 800, gauge_size - 10 * width / 800)
        start_angle = 210 * 16
        span_angle = int(-self.value * 240 / 260 * 16)

        pen = QPen(QColor(int(255 / 260 * self.value), 255 - int(255 / 260 * self.value), 0), int(10 * width / 800))
        painter.setPen(pen)
        painter.drawArc(rect, start_angle, span_angle)

class RPMProgress(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = 0
        self.setFixedSize(gauge_size, gauge_size)

    def setValue(self, value):
        self.value = min(value, 8000)  # Ensure value does not exceed 8000
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(5 * width / 800, 5 * width / 800, gauge_size - 10 * width / 800, gauge_size - 10 * width / 800)
        start_angle = 220 * 16
        span_angle = int(-self.value * 265 / 8000 * 16)  # Scale based on max RPM of 8000

        pen = QPen(QColor(int(255 / 8000 * self.value), 255 - int(255 / 8000 * self.value), 0), int(10 * width / 800))
        painter.setPen(pen)
        painter.drawArc(rect, start_angle, span_angle)

class ClusterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cluster")
        self.setGeometry(0, 0, width, height)

        # Background Image
        self.background_label = QLabel(self)
        self.background_pixmap = QPixmap("image/back.png")
        self.background_label.setPixmap(self.background_pixmap.scaled(width, height, Qt.IgnoreAspectRatio))  # Force scaling to screen size
        self.background_label.setGeometry(0, 0, width, height)
        
		#Speed Gauge
        self.speed_gauge = QLabel(self)
        self.speed_gauge_pixmap = QPixmap("image/dial.png")
        self.speed_gauge.setPixmap(self.speed_gauge_pixmap.scaled(gauge_size, gauge_size, Qt.KeepAspectRatio))
        self.speed_gauge.setGeometry(50, 50, gauge_size, gauge_size)  # Adjusted position and size

        # RPM Gauge
        self.rpm_gauge = QLabel(self)
        self.rpm_gauge_pixmap = QPixmap("image/rpm.png")
        self.rpm_gauge.setPixmap(self.rpm_gauge_pixmap.scaled(gauge_size, gauge_size, Qt.KeepAspectRatio))
        self.rpm_gauge.setGeometry(self.width() - gauge_size - 50, 50, gauge_size, gauge_size)  # Adjusted position and size

        # Speed Progress Widget
        self.speed_progress = SpeedProgress(self)
        self.speed_progress.setGeometry(50, 50, gauge_size, gauge_size)  # Match position and size with speed_gauge

        # RPM Progress Widget
        self.rpm_progress = RPMProgress(self)
        self.rpm_progress.setGeometry(self.width() - gauge_size - 50, 50, gauge_size, gauge_size)  # Match position and size with rpm_gauge

        # Gear State
        gear_label_size = int(150 * width / 1280)  # Scale size relative to screen width
        self.gear_label = QLabel("D", self)
        self.gear_label.setStyleSheet("color:white; font-size: {}px; font-weight: bold;".format(int(130 * width / 1280)))
        self.gear_label.setAlignment(Qt.AlignCenter)
        self.gear_label.setGeometry(
            (self.width() - gear_label_size) // 2,  # Center horizontally
            self.height() - int(250 * height / 720),  # Move slightly higher by increasing the offset
            gear_label_size,  # Width
            gear_label_size   # Height
        )

        # Speed Pointer
        self.current_speed = 260  # Speed value

        # RPM Pointer
        self.current_rpm = 8000  # RPM value

        # Timer for updating pointers
        self.update_timer = QTimer(self)
        self.update_timer.setInterval(100)  # Update every 100ms
        self.update_timer.timeout.connect(self.update_pointers)
        self.update_timer.start()

        # State Variables
        self.show_weather = False
        self.show_warn = False
        self.show_light = False

    def toggle_warn_icon(self):
        self.warn_icon.setVisible(not self.warn_icon.isVisible())

    def toggle_weather(self):
        self.show_weather = not self.show_weather
        self.weather_icon.setVisible(self.show_weather)
        self.temperature_label.setVisible(self.show_weather)

    def toggle_warning(self):
        self.show_warn = not self.show_warn
        if self.show_warn:
            self.blink_timer.start()
        else:
            self.blink_timer.stop()
            self.warn_icon.setVisible(False)

    def toggle_light(self):
        self.show_light = not self.show_light
        self.light_icon.setVisible(self.show_light)

    def update_pointers(self):
        self.speed_progress.setValue(self.current_speed)  # Update SpeedProgress
        self.rpm_progress.setValue(self.current_rpm)      # Update RPMProgress

if __name__ == "__main__":
    window = ClusterWindow()
    window.show()
    sys.exit(app.exec_())

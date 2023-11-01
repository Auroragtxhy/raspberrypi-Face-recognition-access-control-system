# coding: utf-8
from PyQt5 import QtCore, QtGui, QtWidgets  # , QtOpenGL
import math


# 对GUI显示的图片进行操作

class Viewer(QtWidgets.QGraphicsView):
    # 背景区域颜色
    backgroundColor = QtGui.QColor(31, 31, 47)
    # 边框颜色
    borderColor = QtGui.QColor(58, 58, 90)

    sig_position = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        self.setBackgroundBrush(self.backgroundColor)  # 设置背景色

        # self.setDragMode(self.ScrollHandDrag)  # 光标变成指针，拖动鼠标将滚动滚动条。 该模式可以在交互式和非交互式模式下工作

        self.setOptimizationFlag(self.DontSavePainterState)  # 渲染时，不保存 painter 的状态

        self.setRenderHints(
            QtGui.QPainter.Antialiasing | QtGui.QPainter.TextAntialiasing | QtGui.QPainter.SmoothPixmapTransform)  # 设置抗锯齿

        # if QtOpenGL.QGLFormat.hasOpenGL():  # 支持 OpenGL 的系统开始高质量抗锯齿
        #    self.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)

        self.setResizeAnchor(self.AnchorUnderMouse)  # 鼠标当前位置被用作锚点

        # self.setRubberBandSelectionMode(QtCore.Qt.IntersectsItemShape)  # 输出列表包含其形状完全包含在选择区域内的项目以及与区域轮廓相交的项目
        #
        # self.setTransformationAnchor(self.AnchorUnderMouse)  # 鼠标当前位置被用作锚点

        self.setViewportUpdateMode(self.SmartViewportUpdate)  # QGraphicsView将尝试通过分析需要重绘的区域来找到最佳的更新模式。

        self._scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self._scene)

        self._pix_item = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._pix_item)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.last = "Click"

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        """滑轮事件 --- 按下 Ctrl 键时滚动鼠标滚轮时缩放"""
        if event.modifiers() & QtCore.Qt.ControlModifier:
            self.scaleView(math.pow(2.0, event.angleDelta().y() / 240.0))
            return event.accept()
        super(QtWidgets.QGraphicsView, self).wheelEvent(event)

    def scaleView(self, scaleFactor):
        factor = self.transform().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        if factor < 0.07 or factor > 100:
            return
        self.scale(scaleFactor, scaleFactor)

    def display_pix(self, pix: QtGui.QPixmap):
        """更新展示的图片"""
        if not isinstance(pix, QtGui.QPixmap):
            raise TypeError
        self._pix_item.setPixmap(pix)
        if not pix.isNull():
            w, h = pix.width(), pix.height()
            self.fitInView(QtCore.QRectF(0, 0, w, h), QtCore.Qt.KeepAspectRatio)
            self._scene.setSceneRect(0, 0, w, h)
            self._scene.update()
        self.ensureVisible(self._scene.itemsBoundingRect())

    def clear_pix(self):
        """清空显示的图片"""
        self._pix_item.setPixmap(QtGui.QPixmap())

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super(Viewer, self).resizeEvent(event)
        pix = self._pix_item.pixmap()
        if not pix.isNull():
            w, h = pix.width(), pix.height()
            self.fitInView(QtCore.QRectF(0, 0, w, h), QtCore.Qt.KeepAspectRatio)
            self._scene.setSceneRect(0, 0, w, h)
            self._scene.update()
        self.ensureVisible(self._scene.itemsBoundingRect())

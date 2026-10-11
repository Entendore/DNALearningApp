import sys
import math
import random
import json
import os
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QStackedWidget, QFrame, QScrollArea,
    QComboBox, QGroupBox, QGridLayout, QTextEdit, QTableWidget,
    QTableWidgetItem, QProgressBar, QSizePolicy, QSpacerItem,
    QButtonGroup, QRadioButton, QCheckBox, QTabWidget, QSlider,
    QLineEdit, QSpinBox, QInputDialog, QMessageBox, QToolTip,
    QGraphicsDropShadowEffect, QSplitter
)
from PySide6.QtCore import (
    Qt, QTimer, QRectF, QPointF, QPropertyAnimation,
    QEasingCurve, QSize, Signal, QElapsedTimer
)
from PySide6.QtGui import (
    QPainter, QColor, QPen, QBrush, QFont, QLinearGradient,
    QRadialGradient, QPainterPath, QPolygonF, QPixmap, QIcon,
    QFontMetrics, QTextCursor
)

# ─── Color Palette ──────────────────────────────────────────────
COLORS = {
    "bg_dark": "#0a0e1a",
    "bg_medium": "#111827",
    "bg_card": "#1a2236",
    "bg_card_hover": "#1f2a42",
    "accent_blue": "#3b82f6",
    "accent_cyan": "#06b6d4",
    "accent_purple": "#8b5cf6",
    "accent_green": "#10b981",
    "accent_red": "#ef4444",
    "accent_yellow": "#f59e0b",
    "accent_pink": "#ec4899",
    "accent_orange": "#f97316",
    "accent_teal": "#14b8a6",
    "accent_indigo": "#6366f1",
    "text_primary": "#f1f5f9",
    "text_secondary": "#94a3b8",
    "text_muted": "#64748b",
    "base_a": "#10b981",
    "base_t": "#ef4444",
    "base_g": "#f59e0b",
    "base_c": "#3b82f6",
    "base_u": "#8b5cf6",
    "border": "#1e293b",
    "success": "#10b981",
    "warning": "#f59e0b",
    "error": "#ef4444",
}

STYLESHEET = f"""
    QMainWindow {{
        background-color: {COLORS["bg_dark"]};
    }}
    QWidget {{
        color: {COLORS["text_primary"]};
        font-family: 'Segoe UI', Arial, sans-serif;
    }}
    QScrollArea {{
        border: none;
        background: transparent;
    }}
    QScrollBar:vertical {{
        background: {COLORS["bg_dark"]};
        width: 8px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical {{
        background: {COLORS["text_muted"]};
        border-radius: 4px;
        min-height: 30px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QScrollBar:horizontal {{
        background: {COLORS["bg_dark"]};
        height: 8px;
        border-radius: 4px;
    }}
    QScrollBar::handle:horizontal {{
        background: {COLORS["text_muted"]};
        border-radius: 4px;
        min-width: 30px;
    }}
    QTableWidget {{
        background-color: {COLORS["bg_card"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 8px;
        gridline-color: {COLORS["border"]};
        color: {COLORS["text_primary"]};
    }}
    QTableWidget::item {{
        padding: 6px;
    }}
    QHeaderView::section {{
        background-color: {COLORS["bg_medium"]};
        color: {COLORS["text_primary"]};
        padding: 8px;
        border: 1px solid {COLORS["border"]};
        font-weight: bold;
    }}
    QComboBox {{
        background-color: {COLORS["bg_card"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 6px;
        padding: 8px 12px;
        color: {COLORS["text_primary"]};
        min-width: 150px;
    }}
    QComboBox::drop-down {{
        border: none;
    }}
    QComboBox QAbstractItemView {{
        background-color: {COLORS["bg_card"]};
        color: {COLORS["text_primary"]};
        selection-background-color: {COLORS["accent_blue"]};
    }}
    QTextEdit {{
        background-color: {COLORS["bg_card"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 8px;
        padding: 8px;
        color: {COLORS["text_primary"]};
    }}
    QLineEdit {{
        background-color: {COLORS["bg_card"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 6px;
        padding: 8px;
        color: {COLORS["text_primary"]};
    }}
    QLineEdit:focus {{
        border: 2px solid {COLORS["accent_blue"]};
    }}
    QSlider::groove:horizontal {{
        border: 1px solid {COLORS["border"]};
        height: 6px;
        background: {COLORS["bg_card"]};
        border-radius: 3px;
    }}
    QSlider::handle:horizontal {{
        background: {COLORS["accent_blue"]};
        border: none;
        width: 16px;
        height: 16px;
        margin: -5px 0;
        border-radius: 8px;
    }}
    QTabWidget::pane {{
        border: 1px solid {COLORS["border"]};
        background: {COLORS["bg_card"]};
        border-radius: 8px;
    }}
    QTabBar::tab {{
        background: {COLORS["bg_medium"]};
        color: {COLORS["text_secondary"]};
        padding: 10px 20px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        margin-right: 2px;
    }}
    QTabBar::tab:selected {{
        background: {COLORS["bg_card"]};
        color: {COLORS["accent_blue"]};
        font-weight: bold;
    }}
    QRadioButton {{
        color: {COLORS["text_primary"]};
        spacing: 8px;
    }}
    QCheckBox {{
        color: {COLORS["text_primary"]};
        spacing: 8px;
    }}
    QProgressBar {{
        border: 1px solid {COLORS["border"]};
        border-radius: 6px;
        text-align: center;
        background-color: {COLORS["bg_card"]};
        color: {COLORS["text_primary"]};
        height: 20px;
    }}
    QProgressBar::chunk {{
        background-color: {COLORS["accent_green"]};
        border-radius: 5px;
    }}
    QSpinBox {{
        background-color: {COLORS["bg_card"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 6px;
        padding: 6px;
        color: {COLORS["text_primary"]};
    }}
    QToolTip {{
        background-color: {COLORS["bg_card"]};
        color: {COLORS["text_primary"]};
        border: 1px solid {COLORS["accent_blue"]};
        padding: 6px;
        border-radius: 4px;
    }}
"""


# ─── Achievement System ──────────────────────────────────────────

ACHIEVEMENTS = {
    "first_visit": {"name": "🚀 First Steps", "desc": "Opened the app for the first time", "icon": "🚀"},
    "dna_structure": {"name": "🧬 Helix Explorer", "desc": "Visited DNA Structure page", "icon": "🧬"},
    "replication": {"name": "🔄 Replication Master", "desc": "Visited Replication page", "icon": "🔄"},
    "transcription": {"name": "📝 Transcriber", "desc": "Used the transcription simulator", "icon": "📝"},
    "translation": {"name": "🏭 Translator", "desc": "Used the translation simulator", "icon": "🏭"},
    "quiz_5": {"name": "🎯 Quick Learner", "desc": "Answered 5 quiz questions correctly", "icon": "🎯"},
    "quiz_10": {"name": "🏆 DNA Expert", "desc": "Answered 10 quiz questions correctly", "icon": "🏆"},
    "quiz_perfect": {"name": "💎 Perfect Score", "desc": "Got 100% on a quiz", "icon": "💎"},
    "sequence_100": {"name": "🔬 Sequence Pro", "desc": "Analyzed a sequence of 100+ bases", "icon": "🔬"},
    "pcr_run": {"name": "⚡ PCR Runner", "desc": "Ran a PCR simulation", "icon": "⚡"},
    "flashcard_20": {"name": "📚 Flashcard Hero", "desc": "Reviewed 20 flashcards", "icon": "📚"},
    "all_pages": {"name": "🎓 Completionist", "desc": "Visited every page in the app", "icon": "🎓"},
    "gel_run": {"name": "⚡ Gel Runner", "desc": "Ran a gel electrophoresis simulation", "icon": "⚡"},
    "splicing": {"name": "✂️ Splice Master", "desc": "Used the splicing visualizer", "icon": "✂️"},
}


class AchievementManager:
    SAVE_FILE = os.path.join(os.path.expanduser("~"), ".dna_rna_achievements.json")

    def __init__(self):
        self.unlocked = {}
        self.total_correct = 0
        self.flashcards_reviewed = 0
        self.pages_visited = set()
        self.load()

    def load(self):
        try:
            with open(self.SAVE_FILE, 'r') as f:
                data = json.load(f)
                self.unlocked = data.get("unlocked", {})
                self.total_correct = data.get("total_correct", 0)
                self.flashcards_reviewed = data.get("flashcards_reviewed", 0)
                self.pages_visited = set(data.get("pages_visited", []))
        except:
            self.unlocked = {}
            self.total_correct = 0
            self.flashcards_reviewed = 0
            self.pages_visited = set()

    def save(self):
        data = {
            "unlocked": self.unlocked,
            "total_correct": self.total_correct,
            "flashcards_reviewed": self.flashcards_reviewed,
            "pages_visited": list(self.pages_visited),
        }
        try:
            with open(self.SAVE_FILE, 'w') as f:
                json.dump(data, f)
        except:
            pass

    def unlock(self, key):
        if key in ACHIEVEMENTS and key not in self.unlocked:
            self.unlocked[key] = datetime.now().isoformat()
            self.save()
            return True
        return False

    def visit_page(self, page_id):
        self.pages_visited.add(page_id)
        if len(self.pages_visited) >= 14:
            self.unlock("all_pages")
        self.save()

    def add_correct(self, count=1):
        self.total_correct += count
        if self.total_correct >= 5:
            self.unlock("quiz_5")
        if self.total_correct >= 10:
            self.unlock("quiz_10")
        self.save()


achievement_manager = AchievementManager()


# ─── Custom Widgets ──────────────────────────────────────────────

class DNAMHelixWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 400)
        self.offset = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(50)
        self.base_pairs = []
        bp_list = ["A-T", "G-C", "T-A", "C-G", "A-T", "C-G", "G-C", "T-A",
                    "A-T", "G-C", "C-G", "T-A", "A-T", "G-C", "T-A", "C-G",
                    "G-C", "A-T", "T-A", "C-G"]
        for i in range(20):
            pair = bp_list[i % len(bp_list)]
            self.base_pairs.append((pair[0], pair[2]))

    def animate(self):
        self.offset += 2
        if self.offset >= 40:
            self.offset = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        cx = w // 2
        grad = QLinearGradient(0, 0, 0, h)
        grad.setColorAt(0, QColor(COLORS["bg_dark"]))
        grad.setColorAt(1, QColor(COLORS["bg_medium"]))
        painter.fillRect(self.rect(), grad)
        amplitude = min(80, w // 4)
        step = 20
        num_steps = h // step + 2
        for strand in [0, 1]:
            path = QPainterPath()
            started = False
            for i in range(num_steps):
                y = i * step - (self.offset % step)
                phase = strand * math.pi
                x = cx + amplitude * math.sin((y + self.offset * 2) * math.pi / 80 + phase)
                if not started:
                    path.moveTo(x, y)
                    started = True
                else:
                    path.lineTo(x, y)
            color = QColor(COLORS["accent_cyan"]) if strand == 0 else QColor(COLORS["accent_purple"])
            pen = QPen(color, 4)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(path)
        for i in range(num_steps):
            y = i * step - (self.offset % step)
            x1 = cx + amplitude * math.sin((y + self.offset * 2) * math.pi / 80)
            x2 = cx + amplitude * math.sin((y + self.offset * 2) * math.pi / 80 + math.pi)
            z1 = math.cos((y + self.offset * 2) * math.pi / 80)
            if abs(z1) < 0.3:
                continue
            idx = (i + self.offset // step) % len(self.base_pairs)
            base1, base2 = self.base_pairs[idx]
            pen = QPen(QColor(COLORS["text_muted"]), 2, Qt.DashLine)
            painter.setPen(pen)
            painter.drawLine(int(x1), int(y), int(x2), int(y))
            radius = 12
            self._draw_base(painter, x1, y, base1, radius, z1)
            z2 = math.cos((y + self.offset * 2) * math.pi / 80 + math.pi)
            self._draw_base(painter, x2, y, base2, radius, z2)
        legend_y = h - 80
        painter.setFont(QFont("Arial", 9))
        bases_info = [("A", COLORS["base_a"]), ("T", COLORS["base_t"]),
                      ("G", COLORS["base_g"]), ("C", COLORS["base_c"])]
        for j, (b, c) in enumerate(bases_info):
            painter.setBrush(QColor(c))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(10, legend_y + j * 18, 10, 10)
            painter.setPen(QColor(COLORS["text_secondary"]))
            painter.drawText(25, legend_y + j * 18 + 10, f"Base {b}")
        painter.end()

    def _draw_base(self, painter, x, y, base, radius, z):
        base_colors = {"A": COLORS["base_a"], "T": COLORS["base_t"],
                       "G": COLORS["base_g"], "C": COLORS["base_c"],
                       "U": COLORS["base_u"]}
        color = QColor(base_colors.get(base, COLORS["accent_blue"]))
        scale = 0.6 + 0.4 * (z + 1) / 2
        r = int(radius * scale)
        alpha = int(100 + 155 * (z + 1) / 2)
        color.setAlpha(alpha)
        painter.setPen(Qt.NoPen)
        grad = QRadialGradient(x - r * 0.3, y - r * 0.3, r * 1.5)
        grad.setColorAt(0, color.lighter(150))
        grad.setColorAt(1, color)
        painter.setBrush(grad)
        painter.drawEllipse(int(x - r), int(y - r), r * 2, r * 2)
        painter.setPen(QColor(255, 255, 255, alpha))
        painter.setFont(QFont("Arial", max(7, int(9 * scale)), QFont.Bold))
        painter.drawText(int(x - r), int(y - r), r * 2, r * 2, Qt.AlignCenter, base)


class CodonWheelWidget(QWidget):
    """Interactive circular codon wheel."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(450, 450)
        self.hovered_codon = None
        self.setMouseTracking(True)

        self.genetic_code = {
            "UUU": "Phe", "UUC": "Phe", "UUA": "Leu", "UUG": "Leu",
            "CUU": "Leu", "CUC": "Leu", "CUA": "Leu", "CUG": "Leu",
            "AUU": "Ile", "AUC": "Ile", "AUA": "Ile", "AUG": "Met",
            "GUU": "Val", "GUC": "Val", "GUA": "Val", "GUG": "Val",
            "UCU": "Ser", "UCC": "Ser", "UCA": "Ser", "UCG": "Ser",
            "CCU": "Pro", "CCC": "Pro", "CCA": "Pro", "CCG": "Pro",
            "ACU": "Thr", "ACC": "Thr", "ACA": "Thr", "ACG": "Thr",
            "GCU": "Ala", "GCC": "Ala", "GCA": "Ala", "GCG": "Ala",
            "UAU": "Tyr", "UAC": "Tyr", "UAA": "Stop", "UAG": "Stop",
            "CAU": "His", "CAC": "His", "CAA": "Gln", "CAG": "Gln",
            "AAU": "Asn", "AAC": "Asn", "AAA": "Lys", "AAG": "Lys",
            "GAU": "Asp", "GAC": "Asp", "GAA": "Glu", "GAG": "Glu",
            "UGU": "Cys", "UGC": "Cys", "UGA": "Stop", "UGG": "Trp",
            "CGU": "Arg", "CGC": "Arg", "CGA": "Arg", "CGG": "Arg",
            "AGU": "Ser", "AGC": "Ser", "AGA": "Arg", "AGG": "Arg",
            "GGU": "Gly", "GGC": "Gly", "GGA": "Gly", "GGG": "Gly",
        }

        self.aa_colors = {
            "Phe": "#6366f1", "Leu": "#8b5cf6", "Ile": "#a855f7", "Met": "#10b981",
            "Val": "#3b82f6", "Ser": "#06b6d4", "Pro": "#f59e0b", "Thr": "#14b8a6",
            "Ala": "#64748b", "Tyr": "#ec4899", "Stop": "#ef4444", "His": "#f97316",
            "Gln": "#84cc16", "Asn": "#22d3ee", "Lys": "#d946ef", "Asp": "#f43f5e",
            "Glu": "#fb923c", "Cys": "#a3e635", "Trp": "#c084fc", "Arg": "#2dd4bf",
            "Gly": "#94a3b8",
        }
        self._codon_rects = {}

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        r_inner = min(w, h) * 0.12
        r_mid = min(w, h) * 0.28
        r_outer = min(w, h) * 0.42

        painter.fillRect(self.rect(), QColor(COLORS["bg_card"]))

        # Draw rings
        bases = ["U", "C", "A", "G"]
        ring_configs = [
            (r_inner, r_mid, bases, QFont("Consolas", 11, QFont.Bold)),
            (r_mid, r_outer, bases * 4, QFont("Consolas", 9)),
        ]

        # Center label
        painter.setPen(QColor(COLORS["text_primary"]))
        painter.setFont(QFont("Segoe UI", 12, QFont.Bold))
        painter.drawText(QRectF(cx - 30, cy - 12, 60, 24), Qt.AlignCenter, "Codon\nWheel")

        # Draw codon sectors
        codons = list(self.genetic_code.keys())
        angle_per_codon = 360.0 / 64
        self._codon_rects.clear()

        for i, codon in enumerate(codons):
            aa = self.genetic_code[codon]
            color = QColor(self.aa_colors.get(aa, COLORS["accent_blue"]))

            start_angle = i * angle_per_codon
            span = angle_per_codon - 1

            # Outer ring (codon + amino acid)
            path = QPainterPath()
            path.moveTo(cx + r_mid * math.cos(math.radians(start_angle)),
                        cy + r_mid * math.sin(math.radians(start_angle)))
            path.arcTo(QRectF(cx - r_outer, cy - r_outer, r_outer * 2, r_outer * 2),
                       -start_angle - span, span)
            path.arcTo(QRectF(cx - r_mid, cy - r_mid, r_mid * 2, r_mid * 2),
                       -start_angle, -span)
            path.closeSubpath()

            is_hovered = (self.hovered_codon == codon)
            if is_hovered:
                color = color.lighter(150)
            color.setAlpha(is_hovered and 220 or 160)
            painter.setPen(QPen(QColor(COLORS["border"]), 0.5))
            painter.setBrush(color)
            painter.drawPath(path)

            self._codon_rects[codon] = QRectF(
                cx + (r_mid + r_outer) / 2 * math.cos(math.radians(start_angle + span / 2)) - 18,
                cy + (r_mid + r_outer) / 2 * math.sin(math.radians(start_angle + span / 2)) - 8,
                36, 16
            )

            # Label
            mid_r = (r_mid + r_outer) / 2
            mid_angle = math.radians(start_angle + span / 2)
            lx = cx + mid_r * math.cos(mid_angle)
            ly = cy + mid_r * math.sin(mid_angle)
            painter.setPen(QColor(255, 255, 255, 200 if is_hovered else 140))
            painter.setFont(QFont("Consolas", 7, QFont.Bold))
            painter.drawText(QRectF(lx - 16, ly - 6, 32, 12), Qt.AlignCenter, codon)

        # Inner ring - first base
        first_bases = ["U", "C", "A", "G"]
        fb_colors = [COLORS["base_u"], COLORS["base_c"], COLORS["base_a"], COLORS["base_g"]]
        for i, (fb, fbc) in enumerate(zip(first_bases, fb_colors)):
            start_angle = i * 90 + 0.5
            span = 89
            path = QPainterPath()
            path.moveTo(cx, cy)
            path.arcTo(QRectF(cx - r_mid, cy - r_mid, r_mid * 2, r_mid * 2),
                       -start_angle - span, span)
            path.closeSubpath()
            c = QColor(fbc)
            c.setAlpha(100)
            painter.setPen(QPen(QColor(COLORS["border"]), 1))
            painter.setBrush(c)
            painter.drawPath(path)

            mid_angle = math.radians(start_angle + span / 2)
            lx = cx + r_mid * 0.6 * math.cos(mid_angle)
            ly = cy + r_mid * 0.6 * math.sin(mid_angle)
            painter.setPen(QColor(255, 255, 255))
            painter.setFont(QFont("Consolas", 16, QFont.Bold))
            painter.drawText(QRectF(lx - 12, ly - 12, 24, 24), Qt.AlignCenter, fb)

        # Hovered codon info
        if self.hovered_codon and self.hovered_codon in self.genetic_code:
            aa = self.genetic_code[self.hovered_codon]
            aa_color = self.aa_colors.get(aa, COLORS["accent_blue"])
            info_text = f"{self.hovered_codon} → {aa}"
            painter.setPen(QColor(COLORS["text_primary"]))
            painter.setFont(QFont("Segoe UI", 13, QFont.Bold))
            painter.drawText(QRectF(cx - 80, h - 35, 160, 25), Qt.AlignCenter, info_text)

        painter.end()

    def mouseMoveEvent(self, event):
        pos = event.position()
        for codon, rect in self._codon_rects.items():
            if rect.contains(pos):
                if self.hovered_codon != codon:
                    self.hovered_codon = codon
                    self.update()
                    QToolTip.showText(event.globalPosition().toPoint(),
                                      f"{codon} → {self.genetic_code.get(codon, '?')}")
                return
        if self.hovered_codon is not None:
            self.hovered_codon = None
            self.update()
            QToolTip.hideText()


class GelElectrophoresisWidget(QWidget):
    """Gel electrophoresis simulation widget."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 500)
        self.lanes = []  # list of lists of fragment sizes
        self.ladder = [10000, 8000, 6000, 5000, 4000, 3000, 2500, 2000, 1500, 1000, 750, 500, 250, 100]
        self.anim_progress = 1.0
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self._animate_step)
        self.is_animating = False

    def set_lanes(self, lanes):
        self.lanes = lanes
        self.anim_progress = 0.0
        self.is_animating = True
        self.anim_timer.start(30)
        self.update()

    def _animate_step(self):
        self.anim_progress = min(1.0, self.anim_progress + 0.02)
        self.update()
        if self.anim_progress >= 1.0:
            self.anim_timer.stop()
            self.is_animating = False

    def _size_to_y(self, size, top, bottom):
        if size <= 0:
            return bottom
        log_max = math.log10(12000)
        log_min = math.log10(80)
        log_size = math.log10(max(80, min(12000, size)))
        frac = (log_size - log_min) / (log_max - log_min)
        return bottom - frac * (bottom - top)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        # Background - gel
        gel_grad = QLinearGradient(0, 0, 0, h)
        gel_grad.setColorAt(0, QColor("#1a1a2e"))
        gel_grad.setColorAt(0.5, QColor("#16213e"))
        gel_grad.setColorAt(1, QColor("#0f3460"))
        painter.fillRect(self.rect(), gel_grad)

        margin_top = 50
        margin_bottom = 40
        margin_left = 70
        margin_right = 30
        gel_top = margin_top
        gel_bottom = h - margin_bottom

        # Wells
        num_lanes = max(1, len(self.lanes) + 1)  # +1 for ladder
        lane_width = (w - margin_left - margin_right) / num_lanes

        # Draw well slots at top
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 100))
        for i in range(num_lanes):
            wx = margin_left + i * lane_width + lane_width * 0.2
            painter.drawRect(int(wx), gel_top - 5, int(lane_width * 0.6), 10)

        # Draw ladder (lane 0)
        ladder_x = margin_left
        for frag_size in self.ladder:
            y = self._size_to_y(frag_size, gel_top, gel_bottom)
            anim_y = gel_top + (y - gel_top) * self.anim_progress
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(200, 200, 200, 180))
            painter.drawRect(int(ladder_x + 4), int(anim_y - 1), int(lane_width - 8), 3)

            # Size labels
            painter.setPen(QColor(COLORS["text_muted"]))
            painter.setFont(QFont("Consolas", 7))
            if frag_size >= 1000:
                label = f"{frag_size // 1000}kb"
            else:
                label = f"{frag_size}bp"
            painter.drawText(0, int(anim_y - 5), margin_left - 5, 12, Qt.AlignRight | Qt.AlignVCenter, label)

        # Draw sample lanes
        lane_colors = [
            QColor(COLORS["accent_cyan"]),
            QColor(COLORS["accent_green"]),
            QColor(COLORS["accent_purple"]),
            QColor(COLORS["accent_pink"]),
            QColor(COLORS["accent_yellow"]),
        ]
        for lane_idx, fragments in enumerate(self.lanes):
            lane_x = margin_left + (lane_idx + 1) * lane_width
            color = lane_colors[lane_idx % len(lane_colors)]
            for frag_size in fragments:
                y = self._size_to_y(frag_size, gel_top, gel_bottom)
                anim_y = gel_top + (y - gel_top) * self.anim_progress

                # Band glow effect
                glow_color = QColor(color)
                glow_color.setAlpha(30)
                painter.setBrush(glow_color)
                painter.setPen(Qt.NoPen)
                painter.drawRect(int(lane_x + 2), int(anim_y - 5), int(lane_width - 4), 11)

                # Band
                band_color = QColor(color)
                band_color.setAlpha(200)
                painter.setBrush(band_color)
                painter.drawRect(int(lane_x + 4), int(anim_y - 2), int(lane_width - 8), 5)

        # Lane labels
        painter.setPen(QColor(COLORS["text_secondary"]))
        painter.setFont(QFont("Segoe UI", 8))
        painter.drawText(int(margin_left), gel_bottom + 10, int(lane_width), 20,
                         Qt.AlignCenter, "Ladder")
        for i in range(len(self.lanes)):
            lane_x = margin_left + (i + 1) * lane_width
            painter.drawText(int(lane_x), gel_bottom + 10, int(lane_width), 20,
                             Qt.AlignCenter, f"Sample {i + 1}")

        # Title
        painter.setPen(QColor(COLORS["text_primary"]))
        painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
        painter.drawText(10, 20, "Gel Electrophoresis")

        # Direction arrow
        painter.setPen(QPen(QColor(COLORS["text_muted"]), 1))
        painter.setFont(QFont("Segoe UI", 8))
        painter.drawText(5, gel_top + 15, "(-)")
        painter.drawText(5, gel_bottom - 5, "(+)")

        painter.end()


class SplicingVisualizerWidget(QWidget):
    """Visualize RNA splicing - intron removal."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 280)
        self.splicing_step = 0
        self.max_steps = 4
        self.exons = [(0, 80), (140, 220), (280, 360)]
        self.introns = [(80, 140), (220, 280)]
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self._next_step)
        self.is_running = False

    def start_splicing(self):
        self.splicing_step = 0
        self.is_running = True
        self.anim_timer.start(1200)
        self.update()

    def _next_step(self):
        if self.splicing_step < self.max_steps:
            self.splicing_step += 1
            self.update()
        else:
            self.anim_timer.stop()
            self.is_running = False
            achievement_manager.unlock("splicing")

    def reset(self):
        self.anim_timer.stop()
        self.is_running = False
        self.splicing_step = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        painter.fillRect(self.rect(), QColor(COLORS["bg_card"]))

        # Title
        painter.setPen(QColor(COLORS["text_primary"]))
        painter.setFont(QFont("Segoe UI", 12, QFont.Bold))
        step_labels = [
            "Pre-mRNA (Before Splicing)",
            "Spliceosome Binding",
            "Intron Looping (Lariat Formation)",
            "Intron Removal",
            "Mature mRNA (Exons Joined)"
        ]
        painter.drawText(10, 22, step_labels[min(self.splicing_step, 4)])

        # Draw pre-mRNA
        y_main = 70
        total_w = 380
        x_start = (w - total_w) // 2

        # Scale exons/introns to total_w
        exon_colors = [QColor(COLORS["accent_cyan"]), QColor(COLORS["accent_green"]),
                       QColor(COLORS["accent_purple"])]
        intron_color = QColor(COLORS["accent_red"])
        intron_color.setAlpha(150)

        segments = [
            ("exon", 0, 80), ("intron", 80, 140), ("exon", 140, 220),
            ("intron", 220, 280), ("exon", 280, 360)
        ]

        bar_h = 28

        # Draw main RNA bar
        for seg_type, start, end in segments:
            x1 = x_start + (start / 360) * total_w
            x2 = x_start + (end / 360) * total_w
            if seg_type == "exon":
                exon_idx = [s[0] for s in enumerate(segments) if s[1][0] == "exon"]
                idx = 0
                for ei, s in enumerate(segments):
                    if s[0] == "exon" and s[1] == start and s[2] == end:
                        idx = ei
                        break
                color = exon_colors[min(idx, len(exon_colors) - 1)]
                painter.setPen(QPen(color.darker(120), 1))
                grad = QLinearGradient(x1, y_main, x1, y_main + bar_h)
                grad.setColorAt(0, color.lighter(130))
                grad.setColorAt(1, color)
                painter.setBrush(grad)
                painter.drawRoundedRect(int(x1), y_main, int(x2 - x1), bar_h, 4, 4)
                painter.setPen(QColor(255, 255, 255))
                painter.setFont(QFont("Segoe UI", 9, QFont.Bold))
                painter.drawText(int(x1), y_main, int(x2 - x1), bar_h,
                                 Qt.AlignCenter, f"Exon {idx + 1}")
            else:
                intr_idx = 0
                for ii, s in enumerate(segments):
                    if s[0] == "intron" and s[1] == start and s[2] == end:
                        intr_idx = ii
                        break
                should_dim = (self.splicing_step >= 3 and intr_idx <= 1)

                if self.splicing_step == 2 and intr_idx <= 1:
                    # Draw lariat
                    mid_x = (x1 + x2) / 2
                    painter.setPen(QPen(intron_color, 2))
                    painter.setBrush(Qt.NoBrush)
                    loop_path = QPainterPath()
                    loop_path.moveTo(x1, y_main + bar_h)
                    loop_path.cubicTo(x1, y_main + 80, x2, y_main + 80, x2, y_main + bar_h)
                    painter.drawPath(loop_path)
                    # Draw the intron as line
                    painter.setPen(QPen(intron_color, 2, Qt.DashLine))
                    painter.drawLine(int(x1), y_main, int(x2), y_main)
                elif should_dim:
                    # Intron removed - draw dashed outline
                    painter.setPen(QPen(QColor(COLORS["text_muted"]), 1, Qt.DotLine))
                    painter.setBrush(Qt.NoBrush)
                    painter.drawRect(int(x1), y_main, int(x2 - x1), bar_h)
                    painter.setPen(QColor(COLORS["text_muted"]))
                    painter.setFont(QFont("Segoe UI", 8))
                    painter.drawText(int(x1), y_main, int(x2 - x1), bar_h,
                                     Qt.AlignCenter, "removed")
                else:
                    painter.setPen(QPen(intron_color.darker(120), 1))
                    grad = QLinearGradient(x1, y_main, x1, y_main + bar_h)
                    grad.setColorAt(0, intron_color.lighter(130))
                    grad.setColorAt(1, intron_color)
                    painter.setBrush(grad)
                    painter.drawRoundedRect(int(x1), y_main, int(x2 - x1), bar_h, 4, 4)
                    painter.setPen(QColor(255, 255, 255, 200))
                    painter.setFont(QFont("Segoe UI", 8))
                    painter.drawText(int(x1), y_main, int(x2 - x1), bar_h,
                                     Qt.AlignCenter, f"Intron {intr_idx}")

        # Spliceosome indicator
        if self.splicing_step >= 1 and self.splicing_step <= 2:
            for seg_type, start, end in segments:
                if seg_type == "intron":
                    x1 = x_start + (start / 360) * total_w
                    x2 = x_start + (end / 360) * total_w
                    mid_x = (x1 + x2) / 2
                    painter.setPen(QPen(QColor(COLORS["accent_yellow"]), 2, Qt.DashLine))
                    painter.setBrush(QColor(COLORS["accent_yellow"]).setAlpha(30) and Qt.NoBrush)
                    painter.setBrush(Qt.NoBrush)
                    painter.drawEllipse(int(mid_x - 25), y_main - 15, 50, bar_h + 30)
                    painter.setPen(QColor(COLORS["accent_yellow"]))
                    painter.setFont(QFont("Segoe UI", 7))
                    painter.drawText(int(mid_x - 25), y_main - 18, 50, 15,
                                     Qt.AlignCenter, "Spliceosome")

        # Draw mature mRNA below
        if self.splicing_step >= 4:
            y_mature = y_main + 100
            mature_x = x_start
            mature_w = 0
            for seg_type, start, end in segments:
                if seg_type == "exon":
                    mature_w += (end - start) / 360 * total_w

            # Draw arrow
            painter.setPen(QPen(QColor(COLORS["text_muted"]), 1))
            painter.setFont(QFont("Segoe UI", 10))
            arrow_y = y_main + bar_h + 15
            painter.drawText(w // 2 - 40, arrow_y, "⬇ Mature mRNA")

            # Draw joined exons
            curr_x = x_start
            for ei, (seg_type, start, end) in enumerate(segments):
                if seg_type == "exon":
                    x1 = curr_x
                    seg_w = (end - start) / 360 * total_w * (360 / (80 + 80 + 80))
                    idx = 0
                    for eii, s in enumerate(segments):
                        if s[0] == "exon" and s[1] == start and s[2] == end:
                            idx = eii
                            break
                    color = exon_colors[min(idx, len(exon_colors) - 1)]
                    grad = QLinearGradient(x1, y_mature, x1, y_mature + bar_h)
                    grad.setColorAt(0, color.lighter(130))
                    grad.setColorAt(1, color)
                    painter.setPen(QPen(color.darker(120), 1))
                    painter.setBrush(grad)
                    painter.drawRoundedRect(int(x1), y_mature, int(seg_w), bar_h, 4, 4)
                    painter.setPen(QColor(255, 255, 255))
                    painter.setFont(QFont("Segoe UI", 9, QFont.Bold))
                    painter.drawText(int(x1), y_mature, int(seg_w), bar_h,
                                     Qt.AlignCenter, f"Exon {idx + 1}")
                    curr_x += seg_w

            # 5' cap and poly-A
            painter.setPen(QColor(COLORS["accent_yellow"]))
            painter.setFont(QFont("Segoe UI", 9))
            painter.drawText(int(x_start - 5), y_mature - 12, "5' Cap")
            painter.drawText(int(curr_x - 5), y_mature - 12, "Poly-A")

            # Cap circle
            painter.setBrush(QColor(COLORS["accent_yellow"]))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(int(x_start - 10), y_mature + 4, 12, 20)

            # Poly-A tail
            painter.setPen(QPen(QColor(COLORS["accent_pink"]), 2))
            for ai in range(8):
                ax = curr_x + 8 + ai * 4
                painter.drawText(int(ax), y_mature + 18, "A")

        # Legend
        ly = h - 30
        painter.setFont(QFont("Segoe UI", 8))
        items = [("Exon", COLORS["accent_cyan"]), ("Intron", COLORS["accent_red"]),
                 ("Spliceosome", COLORS["accent_yellow"])]
        lx = 10
        for label, color in items:
            painter.setBrush(QColor(color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(lx, ly, 10, 10)
            painter.setPen(QColor(COLORS["text_secondary"]))
            painter.drawText(lx + 14, ly + 10, label)
            lx += 90

        painter.end()


class SectionCard(QFrame):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            SectionCard {{
                background-color: {COLORS["bg_card"]};
                border: 1px solid {COLORS["border"]};
                border-radius: 12px;
                padding: 16px;
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        if title:
            lbl = QLabel(title)
            lbl.setFont(QFont("Segoe UI", 16, QFont.Bold))
            lbl.setStyleSheet(f"color: {COLORS['accent_cyan']}; border: none;")
            layout.addWidget(lbl)
        self.content_layout = layout

    def add_widget(self, widget):
        self.content_layout.addWidget(widget)

    def add_layout(self, layout):
        self.content_layout.addLayout(layout)


class InfoLabel(QLabel):
    def __init__(self, text="", highlight=False, parent=None):
        super().__init__(text, parent)
        self.setWordWrap(True)
        if highlight:
            self.setStyleSheet(f"""
                color: {COLORS["accent_cyan"]};
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                background: rgba(6, 182, 212, 0.1);
                border-left: 3px solid {COLORS["accent_cyan"]};
                border-radius: 4px;
            """)
        else:
            self.setStyleSheet(f"""
                color: {COLORS["text_secondary"]};
                font-size: 13px;
                line-height: 1.6;
            """)


class AccentButton(QPushButton):
    def __init__(self, text="", color=None, parent=None):
        super().__init__(text, parent)
        c = color or COLORS["accent_blue"]
        self.setStyleSheet(f"""
            AccentButton {{
                background-color: {c};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 13px;
                font-weight: bold;
            }}
            AccentButton:hover {{
                background-color: {QColor(c).lighter(120).name()};
            }}
            AccentButton:pressed {{
                background-color: {QColor(c).darker(120).name()};
            }}
            AccentButton:disabled {{
                background-color: {COLORS["text_muted"]};
                color: {COLORS["bg_dark"]};
            }}
        """)
        self.setCursor(Qt.PointingHandCursor)


class NavButton(QPushButton):
    def __init__(self, text="", icon_char="", parent=None):
        super().__init__(parent)
        self._selected = False
        self.icon_char = icon_char
        self.text_content = text
        self.setFixedHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(f"  {icon_char}  {text}")
        self._update_style()

    def _update_style(self):
        if self._selected:
            self.setStyleSheet(f"""
                NavButton {{
                    background-color: rgba(59, 130, 246, 0.15);
                    color: {COLORS["accent_blue"]};
                    border: none;
                    border-left: 3px solid {COLORS["accent_blue"]};
                    border-radius: 0 8px 8px 0;
                    padding: 8px 16px;
                    font-size: 13px;
                    font-weight: bold;
                    text-align: left;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                NavButton {{
                    background-color: transparent;
                    color: {COLORS["text_secondary"]};
                    border: none;
                    border-left: 3px solid transparent;
                    border-radius: 0 8px 8px 0;
                    padding: 8px 16px;
                    font-size: 13px;
                    text-align: left;
                }}
                NavButton:hover {{
                    background-color: rgba(59, 130, 246, 0.08);
                    color: {COLORS["text_primary"]};
                }}
            """)

    def set_selected(self, selected):
        self._selected = selected
        self._update_style()


class NotificationPopup(QFrame):
    """Achievement notification popup."""
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        self.setStyleSheet(f"""
            QFrame {{
                background: {COLORS["bg_card"]};
                border: 2px solid {COLORS["accent_yellow"]};
                border-radius: 10px;
                padding: 8px;
            }}
        """)
        layout = QHBoxLayout(self)
        icon = QLabel("🏆")
        icon.setFont(QFont("Segoe UI", 20))
        icon.setStyleSheet("border: none;")
        layout.addWidget(icon)
        lbl = QLabel(text)
        lbl.setWordWrap(True)
        lbl.setStyleSheet(f"color: {COLORS['accent_yellow']}; font-weight: bold; border: none;")
        layout.addWidget(lbl)

        # Auto-hide animation
        self.opacity = 1.0
        self.hide_timer = QTimer()
        self.hide_timer.timeout.connect(self._fade_out)
        self.fade_timer = QTimer()
        self.fade_timer.timeout.connect(self._reduce_opacity)

    def show_notification(self):
        self.show()
        self.hide_timer.start(3000)

    def _fade_out(self):
        self.hide_timer.stop()
        self.fade_timer.start(30)

    def _reduce_opacity(self):
        self.opacity -= 0.05
        if self.opacity <= 0:
            self.fade_timer.stop()
            self.hide()
            self.opacity = 1.0
        self.setWindowOpacity(self.opacity)


# ─── Page Widgets ────────────────────────────────────────────────

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(24)
        layout.setContentsMargins(32, 24, 32, 24)

        hero = SectionCard()
        h_layout = QHBoxLayout()
        text_layout = QVBoxLayout()
        title = QLabel("🧬 Learn DNA & RNA")
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']}; border: none;")
        subtitle = QLabel(
            "Explore the fascinating world of molecular biology.\n"
            "From DNA structure to protein synthesis — learn it all interactively."
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 15px; border: none;")
        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        # Stats
        unlocked = len(achievement_manager.unlocked)
        total = len(ACHIEVEMENTS)
        stats_label = QLabel(f"🏆 Achievements: {unlocked}/{total}  |  ✅ Quiz Score: {achievement_manager.total_correct}")
        stats_label.setStyleSheet(f"color: {COLORS['accent_yellow']}; font-size: 13px; border: none;")
        text_layout.addWidget(stats_label)
        text_layout.addStretch()

        helix = DNAMHelixWidget()
        helix.setFixedSize(320, 400)
        h_layout.addLayout(text_layout, 1)
        h_layout.addWidget(helix, 0)
        hero.add_layout(h_layout)
        layout.addWidget(hero)

        # Quick nav cards
        stats_layout = QHBoxLayout()
        sections = [
            ("📐", "DNA Structure", "Double helix & nucleotides"),
            ("🔄", "Replication", "Semi-conservative process"),
            ("📝", "Transcription", "DNA → mRNA synthesis"),
            ("🏭", "Translation", "mRNA → Protein"),
            ("🔬", "Sequence Tools", "Analyze DNA sequences"),
            ("🎡", "Codon Wheel", "Interactive codon lookup"),
        ]
        for icon, stitle, desc in sections:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background: {COLORS["bg_card"]};
                    border: 1px solid {COLORS["border"]};
                    border-radius: 10px;
                    padding: 14px;
                }}
                QFrame:hover {{ border-color: {COLORS["accent_blue"]}; }}
            """)
            cl = QVBoxLayout(card)
            il = QLabel(icon)
            il.setFont(QFont("Segoe UI", 22))
            il.setStyleSheet("border: none;")
            il.setAlignment(Qt.AlignCenter)
            tl = QLabel(stitle)
            tl.setFont(QFont("Segoe UI", 11, QFont.Bold))
            tl.setStyleSheet(f"color: {COLORS['accent_cyan']}; border: none;")
            tl.setAlignment(Qt.AlignCenter)
            dl = QLabel(desc)
            dl.setWordWrap(True)
            dl.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px; border: none;")
            dl.setAlignment(Qt.AlignCenter)
            cl.addWidget(il)
            cl.addWidget(tl)
            cl.addWidget(dl)
            stats_layout.addWidget(card)
        layout.addLayout(stats_layout)

        # Key facts
        facts_card = SectionCard("🔬 Key Facts About DNA")
        facts = [
            "🔵 DNA stands for Deoxyribonucleic Acid",
            "🔵 Human DNA has ~3.2 billion base pairs",
            "🔵 If stretched out, DNA from one cell ≈ 2 meters long",
            "🔵 Watson & Crick discovered the double helix in 1953",
            "🔵 99.9% of DNA is identical between all humans",
            "🔵 DNA is replicated at ~1000 bases/second in humans",
        ]
        for f in facts:
            fl = QLabel(f)
            fl.setWordWrap(True)
            fl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px; padding: 3px 0; border: none;")
            facts_card.add_widget(fl)
        layout.addWidget(facts_card)
        layout.addStretch()


class DNAStructurePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(32, 24, 32, 24)

        title = QLabel("📐 DNA Structure")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};")
        layout.addWidget(title)

        content = QHBoxLayout()
        helix_card = SectionCard("Interactive Double Helix")
        helix = DNAMHelixWidget()
        helix.setMinimumSize(300, 450)
        helix_card.add_widget(helix)
        content.addWidget(helix_card, 1)

        right_layout = QVBoxLayout()
        nuc_card = SectionCard("Nucleotide Structure")
        nuc_card.add_widget(InfoLabel("Each DNA nucleotide consists of three components:", True))
        components = [
            ("1️⃣  Phosphate Group", "Contains phosphorus and oxygen. Forms the backbone via phosphodiester bonds.", COLORS["accent_yellow"]),
            ("2️⃣  Deoxyribose Sugar", "A 5-carbon sugar lacking oxygen at 2' position. Connects phosphate to base.", COLORS["accent_green"]),
            ("3️⃣  Nitrogenous Base", "One of four: Adenine (A), Thymine (T), Guanine (G), Cytosine (C).", COLORS["accent_cyan"]),
        ]
        for ct, cd, cc in components:
            frame = QFrame()
            frame.setStyleSheet(f"""
                QFrame {{
                    background: rgba({QColor(cc).red()},{QColor(cc).green()},{QColor(cc).blue()},0.08);
                    border-left: 3px solid {cc};
                    border-radius: 6px; padding: 10px;
                }}
            """)
            fl = QVBoxLayout(frame)
            tl = QLabel(ct); tl.setFont(QFont("Segoe UI", 12, QFont.Bold)); tl.setStyleSheet(f"color: {cc}; border: none;")
            dl = QLabel(cd); dl.setWordWrap(True); dl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; border: none;")
            fl.addWidget(tl); fl.addWidget(dl)
            nuc_card.add_widget(frame)
        right_layout.addWidget(nuc_card)

        bp_card = SectionCard("Base Pairing Rules")
        bp_card.add_widget(InfoLabel("Chargaff's Rules: A=T (2 H-bonds), G≡C (3 H-bonds)"))
        bp_grid = QGridLayout()
        pairs = [
            ("Adenine (A)", "Thymine (T)", "2 H-bonds", COLORS["base_a"], COLORS["base_t"]),
            ("Guanine (G)", "Cytosine (C)", "3 H-bonds", COLORS["base_g"], COLORS["base_c"]),
        ]
        for row, (b1, b2, bonds, c1, c2) in enumerate(pairs):
            l1 = QLabel(f"  {b1}  "); l1.setAlignment(Qt.AlignCenter); l1.setFont(QFont("Segoe UI", 12, QFont.Bold))
            l1.setStyleSheet(f"background: {c1}; color: white; border-radius: 8px; padding: 8px;")
            arrow = QLabel("⇌"); arrow.setAlignment(Qt.AlignCenter); arrow.setFont(QFont("Segoe UI", 18, QFont.Bold))
            arrow.setStyleSheet(f"color: {COLORS['text_muted']};")
            l2 = QLabel(f"  {b2}  "); l2.setAlignment(Qt.AlignCenter); l2.setFont(QFont("Segoe UI", 12, QFont.Bold))
            l2.setStyleSheet(f"background: {c2}; color: white; border-radius: 8px; padding: 8px;")
            bl = QLabel(f"({bonds})"); bl.setAlignment(Qt.AlignCenter); bl.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
            bp_grid.addWidget(l1, row, 0); bp_grid.addWidget(arrow, row, 1)
            bp_grid.addWidget(l2, row, 2); bp_grid.addWidget(bl, row, 3)
        bp_card.add_layout(bp_grid)
        bp_card.add_widget(InfoLabel(
            "📌 Purines (double ring): A & G\n📌 Pyrimidines (single ring): T & C\n📌 Purine always pairs with pyrimidine → constant helix width"
        ))
        right_layout.addWidget(bp_card)
        right_layout.addStretch()
        content.addLayout(right_layout, 1)
        layout.addLayout(content)

        anti_card = SectionCard("Antiparallel Strands")
        anti_card.add_widget(InfoLabel(
            "DNA strands run opposite: 5'→3' and 3'→5'\n"
            "5' end has phosphate; 3' end has hydroxyl group.\n"
            "Essential for replication and transcription directionality."
        ))
        layout.addWidget(anti_card)
        layout.addStretch()


class ReplicationPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(32, 24, 32, 24)
        title = QLabel("🔄 DNA Replication")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold)); title.setStyleSheet(f"color: {COLORS['text_primary']};")
        layout.addWidget(title)

        overview = SectionCard("Overview")
        overview.add_widget(InfoLabel(
            "DNA replication copies DNA before cell division. Semi-conservative: each new DNA has one old + one new strand.", True))
        layout.addWidget(overview)

        steps_card = SectionCard("Steps of DNA Replication")
        steps = [
            ("1️⃣  Origin of Replication", COLORS["accent_blue"], "Replication begins at origins (ori). Helicase unwinds, creating a replication bubble."),
            ("2️⃣  Unwinding (Helicase)", COLORS["accent_cyan"], "Helicase breaks H-bonds. SSBs prevent re-annealing. Topoisomerase relieves tension."),
            ("3️⃣  Primer Synthesis (Primase)", COLORS["accent_green"], "Primase makes short RNA primers. DNA Pol can't start without a primer."),
            ("4️⃣  Elongation (DNA Polymerase)", COLORS["accent_yellow"],
             "DNA Pol III adds nucleotides 5'→3'.\n• Leading strand: continuous\n• Lagging strand: Okazaki fragments"),
            ("5️⃣  Primer Removal", COLORS["accent_purple"], "DNA Pol I removes RNA primers, replaces with DNA."),
            ("6️⃣  Ligation (DNA Ligase)", COLORS["accent_pink"], "DNA Ligase seals gaps between Okazaki fragments."),
            ("7️⃣  Proofreading", COLORS["accent_red"], "3'→5' exonuclease activity. Error rate: ~1 in 10⁹ bp."),
        ]
        for st, sc, sd in steps:
            frame = QFrame()
            frame.setStyleSheet(f"QFrame{{background:{COLORS['bg_medium']};border-left:3px solid {sc};border-radius:6px;padding:12px;}}")
            fl = QVBoxLayout(frame)
            tl = QLabel(st); tl.setFont(QFont("Segoe UI", 13, QFont.Bold)); tl.setStyleSheet(f"color: {sc}; border: none;")
            dl = QLabel(sd); dl.setWordWrap(True); dl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; border: none;")
            fl.addWidget(tl); fl.addWidget(dl)
            steps_card.add_widget(frame)
        layout.addWidget(steps_card)

        enz_card = SectionCard("Key Enzymes")
        table = QTableWidget(); table.setColumnCount(3); table.setRowCount(7)
        table.setHorizontalHeaderLabels(["Enzyme", "Function", "Direction"])
        enzymes = [
            ("Helicase","Unwinds DNA double helix","Both"),("Primase","Synthesizes RNA primers","5'→3'"),
            ("DNA Pol III","Main replication enzyme","5'→3'"),("DNA Pol I","Removes primers, fills gaps","5'→3' & 3'→5'"),
            ("Ligase","Joins Okazaki fragments","N/A"),("Topoisomerase","Relieves supercoiling","Ahead of fork"),
            ("SSB Proteins","Stabilize single strands","N/A")]
        for i,(e,f,d) in enumerate(enzymes):
            table.setItem(i,0,QTableWidgetItem(e)); table.setItem(i,1,QTableWidgetItem(f)); table.setItem(i,2,QTableWidgetItem(d))
        table.resizeColumnsToContents(); enz_card.add_widget(table); layout.addWidget(enz_card)
        layout.addStretch()


class TranscriptionPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(20); layout.setContentsMargins(32, 24, 32, 24)
        title = QLabel("📝 Transcription: DNA → RNA")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold)); title.setStyleSheet(f"color: {COLORS['text_primary']};")
        layout.addWidget(title)

        sim_card = SectionCard("🔬 Interactive Transcription Simulator")
        sim_card.add_widget(InfoLabel("Enter a DNA template strand (3'→5') and see mRNA:"))
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("DNA Template:"))
        self.dna_input = QTextEdit(); self.dna_input.setFixedHeight(40)
        self.dna_input.setPlaceholderText("e.g., TACGGAATC")
        self.dna_input.setStyleSheet(f"QTextEdit{{background:{COLORS['bg_medium']};border:2px solid {COLORS['accent_blue']};border-radius:6px;padding:6px;color:{COLORS['base_a']};font-family:Consolas;font-size:14px;font-weight:bold;}}")
        input_layout.addWidget(self.dna_input, 1)
        btn = AccentButton("🔄 Transcribe", COLORS["accent_green"]); btn.clicked.connect(self.transcribe)
        input_layout.addWidget(btn); sim_card.add_layout(input_layout)

        self.result_frame = QFrame()
        self.result_frame.setStyleSheet(f"QFrame{{background:{COLORS['bg_medium']};border:1px solid {COLORS['border']};border-radius:8px;padding:16px;}}")
        rl = QVBoxLayout(self.result_frame)
        self.dna_display = QLabel(""); self.dna_display.setFont(QFont("Consolas", 14, QFont.Bold))
        self.dna_display.setAlignment(Qt.AlignCenter); self.dna_display.setStyleSheet("border: none;")
        rl.addWidget(self.dna_display)
        self.mrna_display = QLabel(""); self.mrna_display.setFont(QFont("Consolas", 14, QFont.Bold))
        self.mrna_display.setAlignment(Qt.AlignCenter); self.mrna_display.setStyleSheet("border: none;")
        rl.addWidget(self.mrna_display)
        self.info_display = QLabel(""); self.info_display.setWordWrap(True)
        self.info_display.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; border: none;")
        rl.addWidget(self.info_display); sim_card.add_widget(self.result_frame); layout.addWidget(sim_card)

        steps_card = SectionCard("Steps of Transcription")
        for st, sc, sd in [
            ("1️⃣  Initiation", COLORS["accent_blue"], "RNA Pol binds promoter (TATA box). Transcription factors help. DNA unwinds."),
            ("2️⃣  Elongation", COLORS["accent_cyan"], "RNA Pol moves 3'→5' on template, making mRNA 5'→3'. A→U, T→A, G→C, C→G."),
            ("3️⃣  Termination", COLORS["accent_green"], "Prokaryotes: Rho-dependent/independent. Eukaryotes: polyadenylation signal (AAUAAA).")]:
            frame = QFrame(); frame.setStyleSheet(f"QFrame{{background:{COLORS['bg_medium']};border-left:3px solid {sc};border-radius:6px;padding:12px;}}")
            fl = QVBoxLayout(frame); tl = QLabel(st); tl.setFont(QFont("Segoe UI", 13, QFont.Bold)); tl.setStyleSheet(f"color: {sc}; border: none;")
            dl = QLabel(sd); dl.setWordWrap(True); dl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; border: none;")
            fl.addWidget(tl); fl.addWidget(dl); steps_card.add_widget(frame)
        layout.addWidget(steps_card)

        proc_card = SectionCard("Eukaryotic mRNA Processing")
        for pt, pd in [("5' Cap","7-methylguanosine added. Protects mRNA & helps ribosome binding."),
                        ("Poly-A Tail","150-200 adenines added. Aids stability & export."),
                        ("RNA Splicing","Introns removed by spliceosome. Exons joined. Alternative splicing → multiple proteins from one gene.")]:
            frame = QFrame(); frame.setStyleSheet(f"QFrame{{background:rgba(139,92,246,0.08);border-left:3px solid {COLORS['accent_purple']};border-radius:6px;padding:10px;}}")
            fl = QVBoxLayout(frame); tl = QLabel(pt); tl.setFont(QFont("Segoe UI", 12, QFont.Bold)); tl.setStyleSheet(f"color: {COLORS['accent_purple']}; border: none;")
            dl = QLabel(pd); dl.setWordWrap(True); dl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; border: none;")
            fl.addWidget(tl); fl.addWidget(dl); proc_card.add_widget(frame)
        layout.addWidget(proc_card); layout.addStretch()

    def transcribe(self):
        dna = self.dna_input.toPlainText().upper().strip()
        if not dna: return
        complement = {"A": "U", "T": "A", "G": "C", "C": "G"}
        mrna = ""; valid = True
        for base in dna:
            if base in complement: mrna += complement[base]
            else: valid = False; break
        if not valid:
            self.dna_display.setText("❌ Invalid! Use A, T, G, C only")
            self.dna_display.setStyleSheet(f"color: {COLORS['accent_red']}; border: none; font-family: Consolas; font-size: 14px; font-weight: bold;")
            self.mrna_display.setText(""); self.info_display.setText(""); return
        self.dna_display.setText(f"DNA  3'-{dna}-5'")
        self.dna_display.setStyleSheet(f"color: {COLORS['accent_cyan']}; border: none; font-family: Consolas; font-size: 14px; font-weight: bold;")
        self.mrna_display.setText(f"mRNA 5'-{mrna}-3'")
        self.mrna_display.setStyleSheet(f"color: {COLORS['accent_green']}; border: none; font-family: Consolas; font-size: 14px; font-weight: bold;")
        self.info_display.setText(f"✅ {len(dna)} nucleotides transcribed. A→U, T→A, G→C, C→G")
        achievement_manager.unlock("transcription")


class TranslationPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self); layout.setSpacing(20); layout.setContentsMargins(32, 24, 32, 24)
        title = QLabel("🏭 Translation: RNA → Protein")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold)); title.setStyleSheet(f"color: {COLORS['text_primary']};")
        layout.addWidget(title)

        sim_card = SectionCard("🔬 Translation Simulator")
        sim_card.add_widget(InfoLabel("Enter mRNA and translate to amino acids:"))
        input_layout = QHBoxLayout(); input_layout.addWidget(QLabel("mRNA (5'→3'):"))
        self.mrna_input = QTextEdit(); self.mrna_input.setFixedHeight(40)
        self.mrna_input.setPlaceholderText("e.g., AUGGCUAAC")
        self.mrna_input.setStyleSheet(f"QTextEdit{{background:{COLORS['bg_medium']};border:2px solid {COLORS['accent_green']};border-radius:6px;padding:6px;color:{COLORS['accent_cyan']};font-family:Consolas;font-size:14px;font-weight:bold;}}")
        input_layout.addWidget(self.mrna_input, 1)
        btn = AccentButton("🏭 Translate", COLORS["accent_purple"]); btn.clicked.connect(self.translate)
        input_layout.addWidget(btn); sim_card.add_layout(input_layout)
        self.protein_display = QLabel(""); self.protein_display.setWordWrap(True)
        self.protein_display.setFont(QFont("Consolas", 12, QFont.Bold))
        self.protein_display.setStyleSheet(f"color: {COLORS['accent_yellow']}; padding: 12px; border: none;")
        sim_card.add_widget(self.protein_display)
        self.translation_detail = QLabel(""); self.translation_detail.setWordWrap(True)
        self.translation_detail.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; border: none;")
        sim_card.add_widget(self.translation_detail); layout.addWidget(sim_card)

        steps_card = SectionCard("Steps of Translation")
        for st, sc, sd in [
            ("1️⃣  Initiation", COLORS["accent_blue"], "Small ribosomal subunit + mRNA → finds AUG → initiator tRNA (Met) → large subunit joins. A, P, E sites formed."),
            ("2️⃣  Elongation", COLORS["accent_cyan"], "1) Aminoacyl-tRNA enters A site\n2) Peptidyl transferase forms peptide bond\n3) Ribosome translocates\n4) Empty tRNA exits E site"),
            ("3️⃣  Termination", COLORS["accent_green"], "Stop codon (UAA/UAG/UGA) → release factor → polypeptide released → ribosome dissociates.")]:
            frame = QFrame(); frame.setStyleSheet(f"QFrame{{background:{COLORS['bg_medium']};border-left:3px solid {sc};border-radius:6px;padding:12px;}}")
            fl = QVBoxLayout(frame); tl = QLabel(st); tl.setFont(QFont("Segoe UI", 13, QFont.Bold)); tl.setStyleSheet(f"color: {sc}; border: none;")
            dl = QLabel(sd); dl.setWordWrap(True); dl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; border: none;")
            fl.addWidget(tl); fl.addWidget(dl); steps_card.add_widget(frame)
        layout.addWidget(steps_card); layout.addStretch()

    def translate(self):
        gc = {"UUU":"Phe","UUC":"Phe","UUA":"Leu","UUG":"Leu","CUU":"Leu","CUC":"Leu","CUA":"Leu","CUG":"Leu",
              "AUU":"Ile","AUC":"Ile","AUA":"Ile","AUG":"Met","GUU":"Val","GUC":"Val","GUA":"Val","GUG":"Val",
              "UCU":"Ser","UCC":"Ser","UCA":"Ser","UCG":"Ser","CCU":"Pro","CCC":"Pro","CCA":"Pro","CCG":"Pro",
              "ACU":"Thr","ACC":"Thr","ACA":"Thr","ACG":"Thr","GCU":"Ala","GCC":"Ala","GCA":"Ala","GCG":"Ala",
              "UAU":"Tyr","UAC":"Tyr","UAA":"Stop","UAG":"Stop","CAU":"His","CAC":"His","CAA":"Gln","CAG":"Gln",
              "AAU":"Asn","AAC":"Asn","AAA":"Lys","AAG":"Lys","GAU":"Asp","GAC":"Asp","GAA":"Glu","GAG":"Glu",
              "UGU":"Cys","UGC":"Cys","UGA":"Stop","UGG":"Trp","CGU":"Arg","CGC":"Arg","CGA":"Arg","CGG":"Arg",
              "AGU":"Ser","AGC":"Ser","AGA":"Arg","AGG":"Arg","GGU":"Gly","GGC":"Gly","GGA":"Gly","GGG":"Gly"}
        mrna = self.mrna_input.toPlainText().upper().strip().replace(" ", "")
        if not mrna: return
        protein = []; details = []; i = 0
        while i + 2 < len(mrna):
            codon = mrna[i:i+3]
            if codon in gc:
                aa = gc[codon]
                if aa == "Stop": details.append(f"{codon}→STOP"); break
                protein.append(aa); details.append(f"{codon}→{aa}")
            else: details.append(f"{codon}→???"); break
            i += 3
        if protein:
            self.protein_display.setText("Protein: " + " — ".join(protein))
            self.translation_detail.setText(f"✅ {len(protein)} amino acids  |  {'  |  '.join(details)}")
            achievement_manager.unlock("translation")
        else:
            self.protein_display.setText("❌ No valid translation. Start with AUG.")


class RNATypesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self); layout.setSpacing(20); layout.setContentsMargins(32, 24, 32, 24)
        title = QLabel("🧪 Types of RNA"); title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};"); layout.addWidget(title)
        rna_types = [
            ("📨 mRNA", COLORS["accent_blue"], "Carries genetic info from DNA to ribosomes.",
             ["Codon sequence encodes protein","5' cap + poly-A tail","Monocistronic (eukaryotes)","Polycistronic (prokaryotes)"]),
            ("🔗 tRNA", COLORS["accent_green"], "Delivers amino acids during translation. Cloverleaf shape.",
             ["75-90 nucleotides","Anticodon pairs with mRNA codon","CCA 3' end carries amino acid","Wobble position allows flexibility","Unusual bases: inosine, pseudouridine"]),
            ("🏭 rRNA", COLORS["accent_purple"], "Structural & catalytic component of ribosomes. Most abundant RNA.",
             ["~80% of cellular RNA","Eukaryotic: 80S (60S+40S)","Prokaryotic: 70S (50S+30S)","Ribozyme: catalyzes peptide bonds","28S, 18S, 5.8S, 5S in eukaryotes"]),
            ("✂️ snRNA", COLORS["accent_yellow"], "Involved in splicing. Part of spliceosomes.",
             ["U1, U2, U4, U5, U6 form spliceosome","Removes introns from pre-mRNA","Associated with proteins → snRNPs"]),
            ("🛡️ miRNA", COLORS["accent_pink"], "~22 nt. Regulates gene expression post-transcriptionally.",
             ["Binds complementary mRNA","Causes degradation or repression","Regulates ~60% of human genes","Implicated in cancer"]),
            ("🧩 lncRNA", COLORS["accent_red"], ">200 nt non-coding regulatory RNAs.",
             ["X-chromosome inactivation (Xist)","Chromatin remodeling","Molecular scaffolds & decoys"]),
        ]
        for name, color, desc, feats in rna_types:
            card = SectionCard(name); card.add_widget(InfoLabel(desc, True))
            for f in feats:
                fl = QLabel(f"  •  {f}"); fl.setWordWrap(True)
                fl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; padding: 2px 0; border: none;")
                card.add_widget(fl)
            layout.addWidget(card)
        layout.addStretch()


class DNARNAComparisonPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self); layout.setSpacing(20); layout.setContentsMargins(32, 24, 32, 24)
        title = QLabel("⚖️ DNA vs RNA"); title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};"); layout.addWidget(title)
        comp_card = SectionCard("Key Differences")
        table = QTableWidget(); table.setColumnCount(3); table.setRowCount(11)
        table.setHorizontalHeaderLabels(["Feature", "DNA", "RNA"])
        comparisons = [
            ("Full Name","Deoxyribonucleic Acid","Ribonucleic Acid"),("Sugar","Deoxyribose","Ribose"),
            ("Bases","A, T, G, C","A, U, G, C"),("Structure","Double-stranded","Usually single-stranded"),
            ("Shape","Double helix","Various"),("Location","Nucleus & mitochondria","Nucleus & cytoplasm"),
            ("Function","Stores genetic info","Various roles"),("Stability","More stable","Less stable (2' OH)"),
            ("Replication","Self-replicating","From DNA template"),("Length","Millions of bp","70 to thousands nt"),
            ("Catalytic","No","Some are ribozymes")]
        for i,(f,d,r) in enumerate(comparisons):
            fi = QTableWidgetItem(f); fi.setFont(QFont("Segoe UI", 10, QFont.Bold)); table.setItem(i, 0, fi)
            di = QTableWidgetItem(d); di.setForeground(QColor(COLORS["accent_cyan"])); table.setItem(i, 1, di)
            ri = QTableWidgetItem(r); ri.setForeground(QColor(COLORS["accent_purple"])); table.setItem(i, 2, ri)
        table.resizeColumnsToContents(); comp_card.add_widget(table); layout.addWidget(comp_card)

        sim_card = SectionCard("Similarities")
        for s in ["Both are nucleic acids","Both contain A, G, C","Both have sugar-phosphate backbone",
                   "Both involved in gene expression","Both are 5'→3' polymers","Both can store genetic info (some viruses use RNA)"]:
            sl = QLabel(f"  ✅  {s}"); sl.setWordWrap(True)
            sl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px; padding: 4px 0; border: none;")
            sim_card.add_widget(sl)
        layout.addWidget(sim_card)

        dogma_card = SectionCard("📌 Central Dogma")
        dogma_card.add_widget(InfoLabel(
            "DNA → RNA → Protein\n\n1. Replication: DNA → DNA\n2. Transcription: DNA → RNA\n3. Translation: RNA → Protein\n\n"
            "Exceptions:\n• Reverse Transcription: RNA → DNA (retroviruses)\n• RNA Replication: RNA → RNA (RNA viruses)", True))
        layout.addWidget(dogma_card); layout.addStretch()


class MutationsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self); layout.setSpacing(20); layout.setContentsMargins(32, 24, 32, 24)
        title = QLabel("💥 Mutations"); title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};"); layout.addWidget(title)
        overview = SectionCard("What Are Mutations?")
        overview.add_widget(InfoLabel("Permanent changes in DNA sequence. Source of genetic variation. Caused by replication errors, mutagens, or transposons.", True))
        layout.addWidget(overview)

        point_card = SectionCard("Point Mutations")
        for mt, mc, md, subs in [
            ("Substitution", COLORS["accent_blue"], "One base replaced by another.", [
                ("Silent","Same amino acid","accent_green"),("Missense","Different amino acid (e.g., sickle cell)","accent_yellow"),
                ("Nonsense","Creates stop codon","accent_red")]),
            ("Insertion", COLORS["accent_purple"], "Extra nucleotides added. Frameshift if not ×3.", []),
            ("Deletion", COLORS["accent_cyan"], "Nucleotides removed. Frameshift if not ×3.", [])]:
            frame = QFrame(); frame.setStyleSheet(f"QFrame{{background:{COLORS['bg_medium']};border-left:3px solid {mc};border-radius:6px;padding:12px;}}")
            fl = QVBoxLayout(frame); tl = QLabel(f"🔀  {mt}"); tl.setFont(QFont("Segoe UI", 13, QFont.Bold)); tl.setStyleSheet(f"color: {mc}; border: none;")
            dl = QLabel(md); dl.setWordWrap(True); dl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; border: none;")
            fl.addWidget(tl); fl.addWidget(dl)
            for sn, sd, sc in subs:
                sl = QLabel(f"     ↳ {sn}: {sd}"); sl.setWordWrap(True)
                sl.setStyleSheet(f"color: {COLORS[sc]}; font-size: 12px; padding: 2px 0; border: none;")
                fl.addWidget(sl)
            point_card.add_widget(frame)
        layout.addWidget(point_card)

        chrom_card = SectionCard("Chromosomal Mutations")
        for cn, cd, cc in [("Duplication","Segment duplicated","accent_blue"),("Inversion","Segment reversed","accent_cyan"),
                            ("Translocation","Segment moves to another chromosome","accent_purple"),("Deletion","Large segment lost","accent_red")]:
            frame = QFrame(); frame.setStyleSheet(f"QFrame{{background:rgba({QColor(COLORS[cc]).red()},{QColor(COLORS[cc]).green()},{QColor(COLORS[cc]).blue()},0.08);border-left:3px solid {COLORS[cc]};border-radius:6px;padding:10px;}}")
            fl = QVBoxLayout(frame); tl = QLabel(cn); tl.setFont(QFont("Segoe UI", 12, QFont.Bold)); tl.setStyleSheet(f"color: {COLORS[cc]}; border: none;")
            dl = QLabel(cd); dl.setWordWrap(True); dl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; border: none;")
            fl.addWidget(tl); fl.addWidget(dl); chrom_card.add_widget(frame)
        layout.addWidget(chrom_card); layout.addStretch()


class GeneRegulationPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self); layout.setSpacing(20); layout.setContentsMargins(32, 24, 32, 24)
        title = QLabel("🎛️ Gene Regulation"); title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};"); layout.addWidget(title)
        overview = SectionCard("Overview")
        overview.add_widget(InfoLabel("Controls when/how much gene product is made. Allows cell specialization and environmental response.", True))
        layout.addWidget(overview)

        prok_card = SectionCard("🦠 Prokaryotic: The Lac Operon")
        prok_card.add_widget(InfoLabel(
            "Lactose ABSENT: Repressor blocks operator → no transcription\n"
            "Lactose PRESENT: Allolactose binds repressor → transcription ON\n"
            "Glucose PRESENT: Low cAMP → weak transcription (catabolite repression)\n"
            "Glucose ABSENT: High cAMP → CAP activates → strong transcription\n\n"
            "Genes: lacZ (β-galactosidase), lacY (permease), lacA (transacetylase)", True))
        layout.addWidget(prok_card)

        euk_card = SectionCard("🧬 Eukaryotic Regulation")
        for lt, lc, ld in [
            ("1️⃣ Chromatin Remodeling", COLORS["accent_blue"], "Heterochromatin (inactive) vs Euchromatin (active). Histone acetylation/methylation."),
            ("2️⃣ Transcriptional Control", COLORS["accent_cyan"], "Transcription factors bind promoters, enhancers, silencers. Mediator bridges to RNA Pol II."),
            ("3️⃣ Post-Transcriptional", COLORS["accent_green"], "Alternative splicing, mRNA stability, RNA interference (miRNA/siRNA)."),
            ("4️⃣ Translational Control", COLORS["accent_yellow"], "Initiation factor regulation, mRNA localization."),
            ("5️⃣ Post-Translational", COLORS["accent_purple"], "Phosphorylation, ubiquitination, proteasome degradation.")]:
            frame = QFrame(); frame.setStyleSheet(f"QFrame{{background:{COLORS['bg_medium']};border-left:3px solid {lc};border-radius:6px;padding:12px;}}")
            fl = QVBoxLayout(frame); tl = QLabel(lt); tl.setFont(QFont("Segoe UI", 13, QFont.Bold)); tl.setStyleSheet(f"color: {lc}; border: none;")
            dl = QLabel(ld); dl.setWordWrap(True); dl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; border: none;")
            fl.addWidget(tl); fl.addWidget(dl); euk_card.add_widget(frame)
        layout.addWidget(euk_card)

        epi_card = SectionCard("🔬 Epigenetics")
        epi_card.add_widget(InfoLabel(
            "Heritable changes WITHOUT DNA sequence changes.\n\n"
            "• DNA Methylation: Methyl groups on cytosine (CpG). Represses transcription.\n"
            "• Histone Modification: Acetylation (activation), Methylation (varies)\n"
            "• Genomic Imprinting: Only one parent's allele expressed\n"
            "• X-Inactivation: One X silenced in females (Barr body)\n"
            "• Influenced by: environment, diet, stress, aging", True))
        layout.addWidget(epi_card); layout.addStretch()


# ─── NEW FEATURE PAGES ──────────────────────────────────────────

class SequenceAnalyzerPage(QWidget):
    """Comprehensive DNA/RNA sequence analysis tool."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self); layout.setSpacing(20); layout.setContentsMargins(32, 24, 32, 24)
        title = QLabel("🔬 Sequence Analyzer"); title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};"); layout.addWidget(title)

        # Input
        input_card = SectionCard("Input Sequence")
        input_card.add_widget(InfoLabel("Paste a DNA sequence (coding strand, 5'→3'):"))
        self.seq_input = QTextEdit()
        self.seq_input.setPlaceholderText("e.g., ATGGCTAGCTGA...")
        self.seq_input.setMaximumHeight(100)
        self.seq_input.setStyleSheet(f"QTextEdit{{background:{COLORS['bg_medium']};border:2px solid {COLORS['accent_blue']};border-radius:6px;padding:8px;color:{COLORS['accent_cyan']};font-family:Consolas;font-size:13px;font-weight:bold;}}")
        input_card.add_widget(self.seq_input)

        btn_layout = QHBoxLayout()
        for text, color, slot in [
            ("📊 Analyze", COLORS["accent_blue"], self.analyze),
            ("🔄 Complement", COLORS["accent_green"], self.complement),
            ("🔀 Reverse Complement", COLORS["accent_purple"], self.reverse_complement),
            ("📝 Transcribe", COLORS["accent_cyan"], self.transcribe_seq),
            ("🏭 Translate", COLORS["accent_yellow"], self.translate_seq),
            ("✂️ Find ORFs", COLORS["accent_pink"], self.find_orfs),
            ("🔍 Restriction Sites", COLORS["accent_orange"], self.find_restriction_sites),
        ]:
            btn = AccentButton(text, color); btn.clicked.connect(slot); btn_layout.addWidget(btn)
        input_card.add_layout(btn_layout)
        layout.addWidget(input_card)

        # Results
        self.results_card = SectionCard("📊 Results")
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMaximumHeight(450)
        self.results_text.setStyleSheet(f"""
            QTextEdit {{
                background: {COLORS["bg_medium"]};
                border: 1px solid {COLORS["border"]};
                border-radius: 8px;
                padding: 12px;
                color: {COLORS["text_primary"]};
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }}
        """)
        self.results_card.add_widget(self.results_text)
        layout.addWidget(self.results_card)
        layout.addStretch()

    def _clean_seq(self, rna=False):
        seq = self.seq_input.toPlainText().upper().strip().replace(" ", "").replace("\n", "")
        if rna:
            seq = seq.replace("T", "U")
        valid = set("ATGC") if not rna else set("AUGC")
        return "".join(c for c in seq if c in valid)

    def analyze(self):
        seq = self._clean_seq()
        if not seq:
            self.results_text.setHtml("<span style='color:red'>Please enter a valid DNA sequence.</span>"); return
        n = len(seq)
        a = seq.count("A"); t = seq.count("T"); g = seq.count("G"); c = seq.count("C")
        gc = (g + c) / n * 100 if n > 0 else 0
        at = (a + t) / n * 100 if n > 0 else 0
        # Melting temperature (basic Wallace rule for short, nearest-neighbor approximation for longer)
        if n < 14:
            tm = 2 * (a + t) + 4 * (g + c)
        else:
            tm = 64.9 + 41 * (g + c - 16.4) / n
        # Molecular weight (approximate)
        mw = n * 330  # average MW per nucleotide

        # Codons
        codons = [seq[i:i+3] for i in range(0, n - 2, 3)]

        html = f"""
        <h3 style='color:{COLORS["accent_cyan"]}'>📊 Sequence Analysis</h3>
        <table style='color:{COLORS["text_primary"]}'>
        <tr><td><b>Length:</b></td><td>{n:,} bp</td></tr>
        <tr><td><b>A:</b></td><td style='color:{COLORS["base_a"]}'>{a} ({a/n*100:.1f}%)</td></tr>
        <tr><td><b>T:</b></td><td style='color:{COLORS["base_t"]}'>{t} ({t/n*100:.1f}%)</td></tr>
        <tr><td><b>G:</b></td><td style='color:{COLORS["base_g"]}'>{g} ({g/n*100:.1f}%)</td></tr>
        <tr><td><b>C:</b></td><td style='color:{COLORS["base_c"]}'>{c} ({c/n*100:.1f}%)</td></tr>
        <tr><td><b>GC Content:</b></td><td style='color:{COLORS["accent_green"]}'>{gc:.1f}%</td></tr>
        <tr><td><b>AT Content:</b></td><td style='color:{COLORS["accent_yellow"]}'>{at:.1f}%</td></tr>
        <tr><td><b>Melting Temp (Tm):</b></td><td style='color:{COLORS["accent_pink"]}'>{tm:.1f}°C</td></tr>
        <tr><td><b>Approx. MW:</b></td><td>{mw:,} Da ({mw/1000:.1f} kDa)</td></tr>
        <tr><td><b>Codons:</b></td><td>{len(codons)}</td></tr>
        </table>
        <br>
        <b style='color:{COLORS["accent_cyan"]}'>GC Content Interpretation:</b><br>
        <span style='color:{COLORS["text_secondary"]}'>
        {"🟢 Low GC (<40%): AT-rich, lower stability" if gc < 40 else "🟡 Moderate GC (40-60%): typical for many organisms" if gc < 60 else "🔴 High GC (>60%): GC-rich, higher stability"}
        <br>Human genome: ~41% GC | E. coli: ~51% GC | Thermophiles: >60% GC
        </span>
        """
        self.results_text.setHtml(html)
        if n >= 100:
            achievement_manager.unlock("sequence_100")

    def complement(self):
        seq = self._clean_seq()
        comp_map = {"A": "T", "T": "A", "G": "C", "C": "G"}
        comp = "".join(comp_map.get(b, "?") for b in seq)
        self.results_text.setHtml(
            f"<h3 style='color:{COLORS['accent_green']}'>🔄 Complement Strand</h3>"
            f"<p><b>Original  5'→3':</b><br><code style='color:{COLORS['accent_cyan']}'>{seq}</code></p>"
            f"<p><b>Complement 3'→5':</b><br><code style='color:{COLORS['accent_green']}'>{comp}</code></p>")

    def reverse_complement(self):
        seq = self._clean_seq()
        comp_map = {"A": "T", "T": "A", "G": "C", "C": "G"}
        rc = "".join(comp_map.get(b, "?") for b in reversed(seq))
        self.results_text.setHtml(
            f"<h3 style='color:{COLORS['accent_purple']}'>🔀 Reverse Complement</h3>"
            f"<p><b>Original  5'→3':</b><br><code style='color:{COLORS['accent_cyan']}'>{seq}</code></p>"
            f"<p><b>Rev-Comp 5'→3':</b><br><code style='color:{COLORS['accent_purple']}'>{rc}</code></p>")

    def transcribe_seq(self):
        seq = self._clean_seq()
        mrna = seq.replace("T", "U")
        self.results_text.setHtml(
            f"<h3 style='color:{COLORS['accent_cyan']}'>📝 Transcription</h3>"
            f"<p><b>DNA Coding (5'→3'):</b><br><code style='color:{COLORS['accent_cyan']}'>{seq}</code></p>"
            f"<p><b>mRNA (5'→3'):</b><br><code style='color:{COLORS['accent_green']}'>{mrna}</code></p>")

    def translate_seq(self):
        gc = {"UUU":"Phe","UUC":"Phe","UUA":"Leu","UUG":"Leu","CUU":"Leu","CUC":"Leu","CUA":"Leu","CUG":"Leu",
              "AUU":"Ile","AUC":"Ile","AUA":"Ile","AUG":"Met","GUU":"Val","GUC":"Val","GUA":"Val","GUG":"Val",
              "UCU":"Ser","UCC":"Ser","UCA":"Ser","UCG":"Ser","CCU":"Pro","CCC":"Pro","CCA":"Pro","CCG":"Pro",
              "ACU":"Thr","ACC":"Thr","ACA":"Thr","ACG":"Thr","GCU":"Ala","GCC":"Ala","GCA":"Ala","GCG":"Ala",
              "UAU":"Tyr","UAC":"Tyr","UAA":"Stop","UAG":"Stop","CAU":"His","CAC":"His","CAA":"Gln","CAG":"Gln",
              "AAU":"Asn","AAC":"Asn","AAA":"Lys","AAG":"Lys","GAU":"Asp","GAC":"Asp","GAA":"Glu","GAG":"Glu",
              "UGU":"Cys","UGC":"Cys","UGA":"Stop","UGG":"Trp","CGU":"Arg","CGC":"Arg","CGA":"Arg","CGG":"Arg",
              "AGU":"Ser","AGC":"Ser","AGA":"Arg","AGG":"Arg","GGU":"Gly","GGC":"Gly","GGA":"Gly","GGG":"Gly"}
        seq = self._clean_seq()
        mrna = seq.replace("T", "U")
        protein = []; codon_details = []; i = 0
        # Find first AUG
        start = mrna.find("AUG")
        if start < 0:
            self.results_text.setHtml(f"<span style='color:red'>No start codon (AUG) found!</span>"); return
        mrna = mrna[start:]
        while i + 2 < len(mrna):
            codon = mrna[i:i+3]
            if codon in gc:
                aa = gc[codon]
                if aa == "Stop": codon_details.append(f"{codon}→STOP"); break
                protein.append(aa); codon_details.append(f"{codon}→{aa}")
            else: break
            i += 3
        self.results_text.setHtml(
            f"<h3 style='color:{COLORS['accent_yellow']}'>🏭 Translation</h3>"
            f"<p><b>mRNA:</b><br><code>{mrna[:i+3]}</code></p>"
            f"<p><b>Protein ({len(protein)} aa):</b><br><code style='color:{COLORS['accent_yellow']}'>{' — '.join(protein)}</code></p>"
            f"<p><b>Codons:</b><br><code style='color:{COLORS['text_secondary']}'>{' | '.join(codon_details)}</code></p>")

    def find_orfs(self):
        seq = self._clean_seq()
        orfs = []
        for frame in range(3):
            i = frame
            while i + 2 < len(seq):
                codon = seq[i:i+3]
                if codon == "ATG":
                    # Found start, look for stop
                    j = i + 3
                    while j + 2 < len(seq):
                        c = seq[j:j+3]
                        if c in ("TAA", "TAG", "TGA"):
                            orf_len = j + 3 - i
                            orfs.append((i, j + 3, orf_len, frame))
                            break
                        j += 3
                i += 3
        if not orfs:
            self.results_text.setHtml(f"<span style='color:{COLORS['accent_yellow']}'>No ORFs found in this sequence.</span>"); return
        orfs.sort(key=lambda x: x[2], reverse=True)
        html = f"<h3 style='color:{COLORS['accent_pink']}'>✂️ Open Reading Frames</h3>"
        for idx, (start, end, length, frame) in enumerate(orfs[:10]):
            html += f"<p><b>ORF {idx+1}:</b> Frame {frame} | Position {start}-{end} | {length} bp | {length//3} codons<br>"
            html += f"<code style='color:{COLORS['accent_cyan']}'>{seq[start:min(end, start+60)]}{'...' if end-start>60 else ''}</code></p>"
        self.results_text.setHtml(html)

    def find_restriction_sites(self):
        seq = self._clean_seq()
        enzymes = {
            "EcoRI": ("GAATTC", "G|AATTC"), "BamHI": ("GGATCC", "G|GATCC"),
            "HindIII": ("AAGCTT", "A|AGCTT"), "NotI": ("GCGGCCGC", "GC|GGCCGC"),
            "XbaI": ("TCTAGA", "T|CTAGA"), "SalI": ("GTCGAC", "G|TCGAC"),
            "PstI": ("CTGCAG", "CTGCA|G"), "SmaI": ("CCCGGG", "CCC|GGG"),
            "KpnI": ("GGTACC", "GGTAC|C"), "XhoI": ("CTCGAG", "C|TCGAG"),
            "NdeI": ("CATATG", "CA|TATG"), "NcoI": ("CCATGG", "C|CATGG"),
        }
        html = f"<h3 style='color:{COLORS['accent_orange']}'>🔍 Restriction Enzyme Sites</h3>"
        found = 0
        for name, (site, cut) in enzymes.items():
            positions = []
            start = 0
            while True:
                pos = seq.find(site, start)
                if pos < 0: break
                positions.append(pos)
                start = pos + 1
            if positions:
                found += len(positions)
                html += f"<p><b style='color:{COLORS['accent_orange']}'>{name}</b> ({site}): "
                html += f"Found at position(s): {', '.join(str(p) for p in positions)}</p>"
        if found == 0:
            html += f"<p style='color:{COLORS['text_muted']}'>No restriction sites found for the checked enzymes.</p>"
        html += f"<p><b>Total sites found: {found}</b></p>"
        self.results_text.setHtml(html)


class CodonWheelPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self); layout.setSpacing(20); layout.setContentsMargins(32, 24, 32, 24)
        title = QLabel("🎡 Codon Wheel"); title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};"); layout.addWidget(title)

        desc = SectionCard("Interactive Codon Wheel")
        desc.add_widget(InfoLabel(
            "Hover over any sector to see which codon codes for which amino acid. "
            "The inner ring shows the first base, and the outer sectors show complete codons. "
            "Colors represent different amino acids.", True))
        layout.addWidget(desc)

        wheel = CodonWheelWidget()
        wheel.setMinimumSize(500, 500)
        layout.addWidget(wheel, 1)

        # Quick lookup
        lookup_card = SectionCard("🔍 Quick Codon Lookup")
        lookup_layout = QHBoxLayout()
        lookup_layout.addWidget(QLabel("Enter codon:"))
        self.codon_lookup_input = QLineEdit()
        self.codon_lookup_input.setMaxLength(3)
        self.codon_lookup_input.setPlaceholderText("e.g., AUG")
        self.codon_lookup_input.setStyleSheet(f"QLineEdit{{background:{COLORS['bg_medium']};border:2px solid {COLORS['accent_cyan']};border-radius:6px;padding:8px;color:{COLORS['accent_cyan']};font-family:Consolas;font-size:14px;font-weight:bold;}}")
        lookup_layout.addWidget(self.codon_lookup_input, 1)
        btn = AccentButton("Look Up", COLORS["accent_cyan"]); btn.clicked.connect(self.lookup_codon)
        lookup_layout.addWidget(btn)
        lookup_card.add_layout(lookup_layout)
        self.codon_result = QLabel(""); self.codon_result.setWordWrap(True)
        self.codon_result.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold; padding: 8px; border: none;")
        lookup_card.add_widget(self.codon_result)
        layout.addWidget(lookup_card)
        layout.addStretch()

    def lookup_codon(self):
        gc = {"UUU":"Phe","UUC":"Phe","UUA":"Leu","UUG":"Leu","CUU":"Leu","CUC":"Leu","CUA":"Leu","CUG":"Leu",
              "AUU":"Ile","AUC":"Ile","AUA":"Ile","AUG":"Met ▶START","GUU":"Val","GUC":"Val","GUA":"Val","GUG":"Val",
              "UCU":"Ser","UCC":"Ser","UCA":"Ser","UCG":"Ser","CCU":"Pro","CCC":"Pro","CCA":"Pro","CCG":"Pro",
              "ACU":"Thr","ACC":"Thr","ACA":"Thr","ACG":"Thr","GCU":"Ala","GCC":"Ala","GCA":"Ala","GCG":"Ala",
              "UAU":"Tyr","UAC":"Tyr","UAA":"Stop (Ochre)","UAG":"Stop (Amber)","CAU":"His","CAC":"His","CAA":"Gln","CAG":"Gln",
              "AAU":"Asn","AAC":"Asn","AAA":"Lys","AAG":"Lys","GAU":"Asp","GAC":"Asp","GAA":"Glu","GAG":"Glu",
              "UGU":"Cys","UGC":"Cys","UGA":"Stop (Opal)","UGG":"Trp","CGU":"Arg","CGC":"Arg","CGA":"Arg","CGG":"Arg",
              "AGU":"Ser","AGC":"Ser","AGA":"Arg","AGG":"Arg","GGU":"Gly","GGC":"Gly","GGA":"Gly","GGG":"Gly"}
        codon = self.codon_lookup_input.text().upper().strip()
        if codon in gc:
            aa = gc[codon]
            is_start = "START" in aa
            is_stop = "Stop" in aa
            color = COLORS["accent_green"] if is_start else (COLORS["accent_red"] if is_stop else COLORS["accent_cyan"])
            self.codon_result.setText(f"✅ Codon {codon} → <span style='color:{color};font-size:16px;'>{aa}</span>")
        else:
            self.codon_result.setText(f"❌ Invalid codon: {codon}. Use U, C, A, G (3 letters).")


class PCRSimulatorPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cycle = 0
        self.max_cycles = 30
        self.template = "ATGCGATCAAGCTTGAATTCGGATCC"
        self.primers_f = "ATGCGATC"
        self.primers_r = "GGATCC"
        layout = QVBoxLayout(self); layout.setSpacing(20); layout.setContentsMargins(32, 24, 32, 24)
        title = QLabel("⚡ PCR Simulator"); title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};"); layout.addWidget(title)

        info_card = SectionCard("Polymerase Chain Reaction (PCR)")
        info_card.add_widget(InfoLabel(
            "PCR amplifies specific DNA regions exponentially. Each cycle doubles the target DNA.\n\n"
            "3 Steps per Cycle:\n"
            "1️⃣ Denaturation (95°C): DNA strands separate\n"
            "2️⃣ Annealing (55-65°C): Primers bind to template\n"
            "3️⃣ Extension (72°C): Taq polymerase extends primers", True))
        layout.addWidget(info_card)

        # Controls
        ctrl_card = SectionCard("PCR Setup")
        ctrl_layout = QHBoxLayout()

        ctrl_layout.addWidget(QLabel("Template:"))
        self.template_input = QTextEdit()
        self.template_input.setPlainText(self.template)
        self.template_input.setFixedHeight(35)
        self.template_input.setStyleSheet(f"QTextEdit{{background:{COLORS['bg_medium']};border:1px solid {COLORS['border']};border-radius:4px;padding:4px;color:{COLORS['accent_cyan']};font-family:Consolas;font-size:11px;}}")
        ctrl_layout.addWidget(self.template_input, 2)

        ctrl_layout.addWidget(QLabel("Cycles:"))
        self.cycle_spin = QSpinBox()
        self.cycle_spin.setRange(1, 35)
        self.cycle_spin.setValue(25)
        ctrl_layout.addWidget(self.cycle_spin)

        run_btn = AccentButton("▶ Run PCR", COLORS["accent_green"])
        run_btn.clicked.connect(self.run_pcr)
        ctrl_layout.addWidget(run_btn)

        step_btn = AccentButton("⏭ Step", COLORS["accent_blue"])
        step_btn.clicked.connect(self.step_pcr)
        ctrl_layout.addWidget(step_btn)

        reset_btn = AccentButton("🔄 Reset", COLORS["accent_red"])
        reset_btn.clicked.connect(self.reset_pcr)
        ctrl_layout.addWidget(reset_btn)

        ctrl_card.add_layout(ctrl_layout)
        layout.addWidget(ctrl_card)

        # Visual
        self.pcr_visual = QTextEdit()
        self.pcr_visual.setReadOnly(True)
        self.pcr_visual.setMinimumHeight(250)
        self.pcr_visual.setStyleSheet(f"QTextEdit{{background:{COLORS['bg_medium']};border:1px solid {COLORS['border']};border-radius:8px;padding:12px;color:{COLORS['text_primary']};font-family:Consolas;font-size:12px;}}")
        layout.addWidget(self.pcr_visual)

        # Stats
        self.pcr_stats = QLabel("")
        self.pcr_stats.setWordWrap(True)
        self.pcr_stats.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px; padding: 8px; border: none;")
        layout.addWidget(self.pcr_stats)
        layout.addStretch()
        self.reset_pcr()

    def run_pcr(self):
        self.cycle = 0
        self.template = self.template_input.toPlainText().upper().strip().replace(" ", "").replace("\n", "")
        n = self.cycle_spin.value()
        self.pcr_visual.setHtml(self._pcr_html(0))
        self.timer = QTimer()
        self.timer.timeout.connect(self._auto_step)
        self.target_cycles = n
        self.timer.start(400)

    def _auto_step(self):
        if self.cycle < self.target_cycles:
            self.cycle += 1
            self.pcr_visual.setHtml(self._pcr_html(self.cycle))
            self._update_stats()
        else:
            self.timer.stop()
            achievement_manager.unlock("pcr_run")

    def step_pcr(self):
        if self.cycle == 0:
            self.template = self.template_input.toPlainText().upper().strip().replace(" ", "").replace("\n", "")
        self.cycle += 1
        self.pcr_visual.setHtml(self._pcr_html(self.cycle))
        self._update_stats()

    def reset_pcr(self):
        self.cycle = 0
        self.pcr_visual.setHtml(self._pcr_html(0))
        self._update_stats()

    def _update_stats(self):
        n = len(self.template)
        copies = 2 ** self.cycle if self.cycle > 0 else 1
        self.pcr_stats.setText(
            f"📊 Cycle: {self.cycle}  |  Template length: {n} bp  |  "
            f"Target copies: {copies:,}  |  "
            f"Theoretical DNA: {copies * n:,} bp  |  "
            f"Amplification: {copies}x")

    def _pcr_html(self, cycle):
        c = COLORS
        html = f"<h3 style='color:{c['accent_cyan']}'>PCR Cycle Visualization</h3>"

        if cycle == 0:
            html += f"<p style='color:{c['text_secondary']}'>Template DNA (double-stranded):</p>"
            html += f"<p><code style='color:{c['accent_cyan']}'>5'-{self.template}-3'</code></p>"
            comp = "".join({"A":"T","T":"A","G":"C","C":"G"}.get(b,"?") for b in self.template)
            html += f"<p><code style='color:{c['accent_purple']}'>3'-{comp}-5'</code></p>"
            html += f"<p style='color:{c['text_muted']};font-size:11px;'>Press 'Run PCR' or 'Step' to begin amplification.</p>"
            return html

        copies = 2 ** cycle
        html += f"<p style='color:{c['accent_yellow']};font-size:14px;'><b>After Cycle {cycle}: {copies:,} copies</b></p>"

        # Show the 3 steps
        steps_html = [
            ("1️⃣ Denaturation (95°C)", c['accent_red'], "DNA strands separate into single strands"),
            ("2️⃣ Annealing (55-65°C)", c['accent_green'], f"Primers bind to complementary regions"),
            ("3️⃣ Extension (72°C)", c['accent_blue'], f"Taq polymerase extends → new strands synthesized"),
        ]
        for step_name, step_color, step_desc in steps_html:
            html += f"<p><span style='color:{step_color};'><b>{step_name}:</b></span> <span style='color:{c['text_secondary']};font-size:11px;'>{step_desc}</span></p>"

        # Exponential growth visualization
        html += f"<br><p style='color:{c['text_primary']};'><b>Amplification Progress:</b></p>"
        bar_len = min(cycle * 8, 300)
        html += f"<div style='background:{c['accent_green']};width:{bar_len}px;height:16px;border-radius:4px;display:inline-block;'></div>"
        html += f" <span style='color:{c['accent_green']}'>{copies:,}x</span>"

        # Show a few copies
        html += f"<br><br><p style='color:{c['text_muted']};font-size:10px;'>Showing 4 of {copies:,} copies:</p>"
        for i in range(min(4, copies)):
            html += f"<p><code style='color:{c['accent_cyan']};font-size:10px;'>5'-{self.template[:40]}{'...' if len(self.template)>40 else ''}-3'</code></p>"

        return html


class GelElectrophoresisPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self); layout.setSpacing(20); layout.setContentsMargins(32, 24, 32, 24)
        title = QLabel("⚡ Gel Electrophoresis"); title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};"); layout.addWidget(title)

        info_card = SectionCard("How Gel Electrophoresis Works")
        info_card.add_widget(InfoLabel(
            "DNA fragments are separated by size using an electric field through a gel matrix.\n\n"
            "• Smaller fragments move faster (farther)\n"
            "• Larger fragments move slower (stay near top)\n"
            "• DNA is negatively charged → moves toward positive electrode\n"
            "• Agarose concentration affects resolution: 0.7% (large fragments) to 2% (small fragments)", True))
        layout.addWidget(info_card)

        # Input
        ctrl_card = SectionCard("Setup")
        ctrl_layout = QHBoxLayout()
        ctrl_layout.addWidget(QLabel("Add sample (comma-separated bp sizes):"))

        self.sample_inputs = []
        for i in range(4):
            inp = QLineEdit()
            inp.setPlaceholderText(f"Sample {i+1}: e.g., 500,1000,2000")
            inp.setStyleSheet(f"QLineEdit{{background:{COLORS['bg_medium']};border:1px solid {COLORS['border']};border-radius:4px;padding:6px;color:{COLORS['text_primary']};}}")
            ctrl_layout.addWidget(inp)
            self.sample_inputs.append(inp)

        run_btn = AccentButton("⚡ Run Gel", COLORS["accent_green"])
        run_btn.clicked.connect(self.run_gel)
        ctrl_layout.addWidget(run_btn)

        ctrl_card.add_layout(ctrl_layout)

        # Quick presets
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Presets:"))
        for name, samples in [
            ("Lambda HindIII", ["23130,9416,6557,4361,2322,2027,564,125"]),
            ("100bp Ladder", ["100,200,300,400,500,600,700,800,900,1000"]),
            ("Mixed Samples", ["500,1500,3000", "750,2000", "300,900,1800,4000", "1000,2500"]),
        ]:
            btn = AccentButton(name, COLORS["accent_purple"])
            btn.clicked.connect(lambda checked, s=samples: self._set_preset(s))
            preset_layout.addWidget(btn)
        ctrl_card.add_layout(preset_layout)
        layout.addWidget(ctrl_card)

        # Gel widget
        self.gel_widget = GelElectrophoresisWidget()
        self.gel_widget.setMinimumHeight(500)
        layout.addWidget(self.gel_widget)
        layout.addStretch()

    def _set_preset(self, samples):
        for i, s in enumerate(samples):
            if i < len(self.sample_inputs):
                self.sample_inputs[i].setText(s)

    def run_gel(self):
        lanes = []
        for inp in self.sample_inputs:
            text = inp.text().strip()
            if text:
                try:
                    frags = [int(x.strip()) for x in text.split(",") if x.strip().isdigit()]
                    if frags:
                        lanes.append(frags)
                except:
                    pass
        self.gel_widget.set_lanes(lanes)
        achievement_manager.unlock("gel_run")


class SplicingVisualizerPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self); layout.setSpacing(20); layout.setContentsMargins(32, 24, 32, 24)
        title = QLabel("✂️ RNA Splicing Visualizer"); title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};"); layout.addWidget(title)

        info_card = SectionCard("What is RNA Splicing?")
        info_card.add_widget(InfoLabel(
            "In eukaryotes, genes contain introns (non-coding) and exons (coding). During RNA processing, "
            "the spliceosome removes introns and joins exons together to form mature mRNA.\n\n"
            "• Spliceosome: complex of snRNPs (U1, U2, U4, U5, U6)\n"
            "• Alternative splicing: different exon combinations → multiple proteins from one gene\n"
            "• ~95% of human genes undergo alternative splicing", True))
        layout.addWidget(info_card)

        # Visualizer
        viz_card = SectionCard("Splicing Animation")
        self.splicing_widget = SplicingVisualizerWidget()
        self.splicing_widget.setMinimumHeight(280)
        viz_card.add_widget(self.splicing_widget)

        btn_layout = QHBoxLayout()
        start_btn = AccentButton("▶ Start Splicing", COLORS["accent_green"])
        start_btn.clicked.connect(self.splicing_widget.start_splicing)
        btn_layout.addWidget(start_btn)

        reset_btn = AccentButton("🔄 Reset", COLORS["accent_red"])
        reset_btn.clicked.connect(self.splicing_widget.reset)
        btn_layout.addWidget(reset_btn)
        viz_card.add_layout(btn_layout)
        layout.addWidget(viz_card)

        # Alternative splicing
        alt_card = SectionCard("🔀 Alternative Splicing Patterns")
        patterns = [
            ("Constitutive", "All exons included → one protein", COLORS["accent_blue"]),
            ("Exon Skipping", "An exon is skipped → shorter protein", COLORS["accent_cyan"]),
            ("Alternative 5' Splice Site", "Different 5' boundary → exon extended/truncated", COLORS["accent_green"]),
            ("Alternative 3' Splice Site", "Different 3' boundary → exon extended/truncated", COLORS["accent_yellow"]),
            ("Mutually Exclusive Exons", "One of two exons included, not both", COLORS["accent_purple"]),
            ("Intron Retention", "Intron remains → often produces non-functional protein", COLORS["accent_red"]),
        ]
        for pname, pdesc, pcolor in patterns:
            frame = QFrame()
            frame.setStyleSheet(f"QFrame{{background:rgba({QColor(pcolor).red()},{QColor(pcolor).green()},{QColor(pcolor).blue()},0.08);border-left:3px solid {pcolor};border-radius:6px;padding:8px;}}")
            fl = QVBoxLayout(frame)
            tl = QLabel(pname); tl.setFont(QFont("Segoe UI", 11, QFont.Bold)); tl.setStyleSheet(f"color: {pcolor}; border: none;")
            dl = QLabel(pdesc); dl.setWordWrap(True); dl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; border: none;")
            fl.addWidget(tl); fl.addWidget(dl)
            alt_card.add_widget(frame)
        layout.addWidget(alt_card)
        layout.addStretch()


class TimelinePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self); layout.setSpacing(20); layout.setContentsMargins(32, 24, 32, 24)
        title = QLabel("📜 DNA History Timeline"); title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};"); layout.addWidget(title)

        events = [
            ("1866", "Gregor Mendel", "Publishes laws of inheritance based on pea plant experiments", COLORS["accent_blue"]),
            ("1869", "Friedrich Miescher", "Discovers 'nuclein' (DNA) in white blood cell nuclei", COLORS["accent_cyan"]),
            ("1902", "Walter Sutton", "Proposes chromosomes carry hereditary information", COLORS["accent_green"]),
            ("1928", "Frederick Griffith", "Discovers bacterial transformation (rough→smooth pneumonia)", COLORS["accent_yellow"]),
            ("1944", "Avery, MacLeod, McCarty", "Identifies DNA as the transforming principle", COLORS["accent_purple"]),
            ("1950", "Erwin Chargaff", "Discovers Chargaff's rules: A=T, G=C in DNA", COLORS["accent_pink"]),
            ("1952", "Hershey & Chase", "Blender experiment confirms DNA (not protein) is genetic material", COLORS["accent_orange"]),
            ("1953", "Watson & Crick", "Discover the double helix structure of DNA", COLORS["accent_red"]),
            ("1957", "Crick", "Proposes the Central Dogma: DNA → RNA → Protein", COLORS["accent_teal"]),
            ("1961", "Nirenberg & Matthaei", "Crack the genetic code: UUU = Phenylalanine", COLORS["accent_indigo"]),
            ("1966", "Complete Code", "All 64 codons decoded", COLORS["accent_blue"]),
            ("1972", "Paul Berg", "Creates first recombinant DNA molecule", COLORS["accent_cyan"]),
            ("1977", "Sanger & Gilbert", "Develop DNA sequencing methods", COLORS["accent_green"]),
            ("1983", "Kary Mullis", "Invents PCR (Polymerase Chain Reaction)", COLORS["accent_yellow"]),
            ("1990", "Human Genome Project", "13-year international effort to sequence the human genome begins", COLORS["accent_purple"]),
            ("1996", "Dolly the Sheep", "First mammal cloned from adult somatic cell", COLORS["accent_pink"]),
            ("2003", "Human Genome Complete", "Human Genome Project completed — 3.2 billion base pairs mapped", COLORS["accent_orange"]),
            ("2012", "Doudna & Charpentier", "CRISPR-Cas9 gene editing technology published", COLORS["accent_red"]),
            ("2020", "mRNA Vaccines", "First mRNA vaccines (COVID-19) using synthetic mRNA technology", COLORS["accent_teal"]),
            ("2023", "Base Editing", "Precision gene editing without double-strand breaks advances", COLORS["accent_indigo"]),
        ]

        for year, person, desc, color in events:
            frame = QFrame()
            frame.setStyleSheet(f"""
                QFrame {{
                    background: rgba({QColor(color).red()},{QColor(color).green()},{QColor(color).blue()},0.06);
                    border-left: 4px solid {color};
                    border-radius: 8px;
                    padding: 12px;
                }}
                QFrame:hover {{
                    background: rgba({QColor(color).red()},{QColor(color).green()},{QColor(color).blue()},0.12);
                }}
            """)
            fl = QHBoxLayout(frame)
            year_lbl = QLabel(year)
            year_lbl.setFixedWidth(60)
            year_lbl.setFont(QFont("Consolas", 16, QFont.Bold))
            year_lbl.setStyleSheet(f"color: {color}; border: none;")
            year_lbl.setAlignment(Qt.AlignCenter)
            fl.addWidget(year_lbl)

            info_layout = QVBoxLayout()
            person_lbl = QLabel(person)
            person_lbl.setFont(QFont("Segoe UI", 13, QFont.Bold))
            person_lbl.setStyleSheet(f"color: {color}; border: none;")
            desc_lbl = QLabel(desc)
            desc_lbl.setWordWrap(True)
            desc_lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; border: none;")
            info_layout.addWidget(person_lbl)
            info_layout.addWidget(desc_lbl)
            fl.addLayout(info_layout, 1)
            layout.addWidget(frame)

        layout.addStretch()


class ProteinStructurePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(32, 24, 32, 24)
        
        title = QLabel("🏗️ Protein Structure")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};")
        layout.addWidget(title)

        levels = [
            ("1️⃣ Primary Structure", COLORS["accent_blue"],
             "Linear sequence of amino acids linked by peptide bonds.",
             "• Determined by the gene (DNA sequence)\n• Peptide bonds form between carboxyl (-COOH) and amino (-NH₂) groups\n• Direction: N-terminus → C-terminus\n• Even a single amino acid change can alter function (e.g., sickle cell anemia: Glu→Val)"),
            ("2️⃣ Secondary Structure", COLORS["accent_cyan"],
             "Local folding patterns stabilized by hydrogen bonds between backbone atoms.",
             "• α-helix: coiled spring, 3.6 residues/turn, H-bonds between i and i+4\n• β-sheet: extended strands, parallel or antiparallel\n• β-turns: reverse direction of polypeptide chain\n• Ramachandran plot shows allowed φ/ψ angles"),
            ("3️⃣ Tertiary Structure", COLORS["accent_green"],
             "Overall 3D shape of a single polypeptide chain.",
             "• Stabilized by: H-bonds, ionic bonds, hydrophobic interactions, disulfide bridges, Van der Waals\n• Hydrophobic residues fold inward (away from water)\n• Hydrophilic residues face outward\n• Chaperone proteins assist folding\n• Misfolded proteins → diseases (Alzheimer's, prions)"),
            ("4️⃣ Quaternary Structure", COLORS["accent_purple"],
             "Arrangement of multiple polypeptide chains (subunits) into a functional complex.",
             "• Hemoglobin: 4 subunits (2α + 2β)\n• DNA Polymerase III: 10+ subunits\n• Ribosome: 50+ proteins + rRNA\n• Cooperativity: subunit binding affects others\n• Allosteric regulation"),
        ]
        
        for lt, lc, lshort, ldetail in levels:
            card = SectionCard(lt)
            
            # Add the short description
            info_label = InfoLabel(lshort, True)
            card.add_widget(info_label)
            
            # Add the detailed description
            dl = QLabel(ldetail)
            dl.setWordWrap(True)
            dl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; border: none;")
            card.add_widget(dl)
            
            layout.addWidget(card)

        # Amino acid categories
        cat_card = SectionCard("🏷️ Amino Acid Categories")
        categories = [
            ("Nonpolar (Hydrophobic)", "Gly, Ala, Val, Leu, Ile, Pro, Phe, Met, Trp", COLORS["accent_blue"]),
            ("Polar Uncharged", "Ser, Thr, Cys, Tyr, Asn, Gln", COLORS["accent_cyan"]),
            ("Positively Charged", "Lys, Arg, His", COLORS["accent_green"]),
            ("Negatively Charged", "Asp, Glu", COLORS["accent_red"]),
            ("Special Cases", "Cys (disulfide bonds), Pro (kinks), Gly (flexibility)", COLORS["accent_yellow"]),
        ]
        for cat_name, cat_aas, cat_color in categories:
            frame = QFrame()
            frame.setStyleSheet(f"QFrame{{background:rgba({QColor(cat_color).red()},{QColor(cat_color).green()},{QColor(cat_color).blue()},0.08);border-left:3px solid {cat_color};border-radius:6px;padding:8px;}}")
            fl = QVBoxLayout(frame)
            nl = QLabel(cat_name)
            nl.setFont(QFont("Segoe UI", 11, QFont.Bold))
            nl.setStyleSheet(f"color: {cat_color}; border: none;")
            al = QLabel(cat_aas)
            al.setWordWrap(True)
            al.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; border: none;")
            fl.addWidget(nl)
            fl.addWidget(al)
            cat_card.add_widget(frame)
            
        layout.addWidget(cat_card)
        layout.addStretch()


class CellDivisionPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self); layout.setSpacing(20); layout.setContentsMargins(32, 24, 32, 24)
        title = QLabel("🔀 Cell Division"); title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};"); layout.addWidget(title)

        # Mitosis
        mito_card = SectionCard("Mitosis — Somatic Cell Division")
        mito_card.add_widget(InfoLabel("Produces 2 identical diploid daughter cells. For growth and repair.", True))
        mitosis_phases = [
            ("🔬 Prophase", COLORS["accent_blue"], "Chromatin condenses into chromosomes. Nuclear envelope begins to break down. Centrioles move to poles. Spindle fibers form."),
            ("📐 Metaphase", COLORS["accent_cyan"], "Chromosomes align at the metaphase plate (cell equator). Spindle fibers attach to kinetochores. Checkpoint: all chromosomes must be attached."),
            ("↕️ Anaphase", COLORS["accent_green"], "Sister chromatids separate. Pulled to opposite poles by shortening spindle fibers. Cell elongates."),
            ("🔄 Telophase", COLORS["accent_yellow"], "Chromosomes decondense. Nuclear envelopes reform. Spindle breaks down. Cytokinesis begins (cleavage furrow in animals, cell plate in plants)."),
        ]
        for pt, pc, pd in mitosis_phases:
            frame = QFrame(); frame.setStyleSheet(f"QFrame{{background:{COLORS['bg_medium']};border-left:3px solid {pc};border-radius:6px;padding:10px;}}")
            fl = QVBoxLayout(frame); tl = QLabel(pt); tl.setFont(QFont("Segoe UI", 12, QFont.Bold)); tl.setStyleSheet(f"color: {pc}; border: none;")
            dl = QLabel(pd); dl.setWordWrap(True); dl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; border: none;")
            fl.addWidget(tl); fl.addWidget(dl); mito_card.add_widget(frame)
        layout.addWidget(mito_card)

        # Meiosis
        meio_card = SectionCard("Meiosis — Gamete Production")
        meio_card.add_widget(InfoLabel("Produces 4 non-identical haploid gametes. For sexual reproduction.", True))
        meiosis_phases = [
            ("Meiosis I — Reduction Division", COLORS["accent_purple"],
             "• Prophase I: Homologous chromosomes pair (synapsis). Crossing over occurs at chiasmata.\n"
             "• Metaphase I: Homologous pairs align at equator (independent assortment).\n"
             "• Anaphase I: Homologous chromosomes separate (NOT chromatids).\n"
             "• Telophase I: Two haploid cells form. Each has one chromosome from each pair."),
            ("Meiosis II — Equational Division", COLORS["accent_pink"],
             "• Prophase II: Chromosomes condense again.\n"
             "• Metaphase II: Chromosomes align at equator.\n"
             "• Anaphase II: Sister chromatids separate.\n"
             "• Telophase II: 4 haploid cells result."),
        ]
        for pt, pc, pd in meiosis_phases:
            frame = QFrame(); frame.setStyleSheet(f"QFrame{{background:{COLORS['bg_medium']};border-left:3px solid {pc};border-radius:6px;padding:10px;}}")
            fl = QVBoxLayout(frame); tl = QLabel(pt); tl.setFont(QFont("Segoe UI", 12, QFont.Bold)); tl.setStyleSheet(f"color: {pc}; border: none;")
            dl = QLabel(pd); dl.setWordWrap(True); dl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; border: none;")
            fl.addWidget(tl); fl.addWidget(dl); meio_card.add_widget(frame)
        layout.addWidget(meio_card)

        # Comparison
        comp_card = SectionCard("Mitosis vs Meiosis")
        table = QTableWidget(); table.setColumnCount(3); table.setRowCount(7)
        table.setHorizontalHeaderLabels(["Feature", "Mitosis", "Meiosis"])
        comparisons = [
            ("Division","1","2"),("Daughter cells","2","4"),
            ("Ploidy","Diploid (2n)","Haploid (n)"),
            ("Genetically","Identical","Different (crossing over)"),
            ("Occurs in","Somatic cells","Germ cells"),
            ("Purpose","Growth & repair","Gamete production"),
            ("Crossing over","No","Yes (Prophase I)")]
        for i,(f,m,me) in enumerate(comparisons):
            table.setItem(i,0,QTableWidgetItem(f)); table.setItem(i,1,QTableWidgetItem(m)); table.setItem(i,2,QTableWidgetItem(me))
        table.resizeColumnsToContents(); comp_card.add_widget(table); layout.addWidget(comp_card)
        layout.addStretch()


class FlashcardPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cards = self._create_cards()
        self.filtered_cards = self.cards[:] 
        self.current_idx = 0
        self.flipped = False
        self.reviewed = 0

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(32, 24, 32, 24)
        
        title = QLabel("📚 Flashcards")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};")
        layout.addWidget(title)

        # Progress
        self.progress_label = QLabel(f"Card 1 / {len(self.filtered_cards)}")
        self.progress_label.setFont(QFont("Segoe UI", 13))
        self.progress_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(len(self.filtered_cards))
        self.progress_bar.setValue(1)
        layout.addWidget(self.progress_bar)

        # Flashcard
        self.card_frame = QFrame()
        self.card_frame.setStyleSheet(f"""
            QFrame {{
                background: {COLORS["bg_card"]};
                border: 2px solid {COLORS["accent_blue"]};
                border-radius: 16px;
                padding: 32px;
                min-height: 200px;
            }}
        """)
        card_layout = QVBoxLayout(self.card_frame)
        self.card_category = QLabel("")
        self.card_category.setFont(QFont("Segoe UI", 11))
        self.card_category.setStyleSheet(f"color: {COLORS['accent_cyan']}; border: none;")
        card_layout.addWidget(self.card_category)

        self.card_text = QLabel("")
        self.card_text.setWordWrap(True)
        self.card_text.setFont(QFont("Segoe UI", 18))
        self.card_text.setAlignment(Qt.AlignCenter)
        self.card_text.setStyleSheet(f"color: {COLORS['text_primary']}; padding: 20px; border: none;")
        card_layout.addWidget(self.card_text)

        self.card_hint = QLabel("Click to flip")
        self.card_hint.setFont(QFont("Segoe UI", 10))
        self.card_hint.setAlignment(Qt.AlignCenter)
        self.card_hint.setStyleSheet(f"color: {COLORS['text_muted']}; border: none;")
        card_layout.addWidget(self.card_hint)
        layout.addWidget(self.card_frame, 1)

        # Buttons
        btn_layout = QHBoxLayout()
        prev_btn = AccentButton("⬅ Previous", COLORS["accent_purple"])
        prev_btn.clicked.connect(self.prev_card)
        btn_layout.addWidget(prev_btn)

        flip_btn = AccentButton("🔄 Flip Card", COLORS["accent_blue"])
        flip_btn.clicked.connect(self.flip_card)
        btn_layout.addWidget(flip_btn)

        next_btn = AccentButton("Next ➡", COLORS["accent_green"])
        next_btn.clicked.connect(self.next_card)
        btn_layout.addWidget(next_btn)

        shuffle_btn = AccentButton("🔀 Shuffle", COLORS["accent_yellow"])
        shuffle_btn.clicked.connect(self.shuffle_cards)
        btn_layout.addWidget(shuffle_btn)
        layout.addLayout(btn_layout)

        # Category filter
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Category:"))
        self.category_combo = QComboBox()
        categories = ["All"] + sorted(set(c["category"] for c in self.cards))
        self.category_combo.addItems(categories)
        self.category_combo.currentTextChanged.connect(self.filter_cards)
        filter_layout.addWidget(self.category_combo)
        layout.addLayout(filter_layout)

        self._show_card()

    def _create_cards(self):
        return [
            {"q": "What bases does DNA contain?", "a": "Adenine (A), Thymine (T), Guanine (G), Cytosine (C)", "category": "DNA Structure"},
            {"q": "What bases does RNA contain?", "a": "Adenine (A), Uracil (U), Guanine (G), Cytosine (C)", "category": "RNA"},
            {"q": "What is the sugar in DNA?", "a": "Deoxyribose", "category": "DNA Structure"},
            {"q": "What is the sugar in RNA?", "a": "Ribose", "category": "RNA"},
            {"q": "What enzyme unwinds DNA during replication?", "a": "Helicase", "category": "Replication"},
            {"q": "What enzyme synthesizes RNA from DNA?", "a": "RNA Polymerase", "category": "Transcription"},
            {"q": "What is the start codon?", "a": "AUG (Methionine)", "category": "Translation"},
            {"q": "What are the stop codons?", "a": "UAA, UAG, UGA", "category": "Translation"},
            {"q": "What carries amino acids to the ribosome?", "a": "tRNA (Transfer RNA)", "category": "RNA"},
            {"q": "What is a mutation where one base replaces another?", "a": "Substitution (or Point Mutation)", "category": "Mutations"},
            {"q": "What are introns and exons?", "a": "Introns = non-coding, Exons = coding sequences", "category": "Gene Regulation"},
            {"q": "What is the structure of DNA?", "a": "Double Helix", "category": "DNA Structure"},
            {"q": "What bond joins nucleotides in the backbone?", "a": "Phosphodiester bond", "category": "DNA Structure"},
            {"q": "How many hydrogen bonds between A and T?", "a": "2 hydrogen bonds", "category": "DNA Structure"},
            {"q": "How many hydrogen bonds between G and C?", "a": "3 hydrogen bonds", "category": "DNA Structure"},
            {"q": "Who discovered the double helix?", "a": "Watson and Crick (1953)", "category": "History"},
            {"q": "What is PCR?", "a": "Polymerase Chain Reaction - amplifies DNA exponentially", "category": "Techniques"},
            {"q": "What is the purpose of Gel Electrophoresis?", "a": "To separate DNA fragments by size", "category": "Techniques"},
            {"q": "What is the central dogma?", "a": "DNA → RNA → Protein", "category": "Central Dogma"},
            {"q": "What is semi-conservative replication?", "a": "Each new DNA molecule has one old and one new strand", "category": "Replication"},
            {"q": "What joins Okazaki fragments?", "a": "DNA Ligase", "category": "Replication"},
            {"q": "What are the 3 steps of translation?", "a": "Initiation, Elongation, Termination", "category": "Translation"},
            {"q": "What is a frameshift mutation?", "a": "Insertion or deletion of bases not divisible by 3", "category": "Mutations"},
            {"q": "What is epigenetics?", "a": "Heritable changes in gene expression without DNA sequence changes", "category": "Gene Regulation"},
            {"q": "What are snRNPs?", "a": "Small nuclear Ribonucleoproteins - form the spliceosome", "category": "RNA"},
        ]

    def _show_card(self):
        if not self.filtered_cards:
            self.card_text.setText("No cards in this category")
            return
        card = self.filtered_cards[self.current_idx]
        self.flipped = False
        self.card_category.setText(f"📂 {card['category']}")
        self.card_text.setText(f"❓ {card['q']}")
        self.card_hint.setText("Click 'Flip Card' to see the answer")
        self.card_frame.setStyleSheet(f"""
            QFrame {{
                background: {COLORS["bg_card"]};
                border: 2px solid {COLORS["accent_blue"]};
                border-radius: 16px;
                padding: 32px;
                min-height: 200px;
            }}
        """)
        self.progress_label.setText(f"Card {self.current_idx + 1} / {len(self.filtered_cards)}")
        self.progress_bar.setValue(self.current_idx + 1)

    def flip_card(self):
        if not self.filtered_cards: return
        self.flipped = not self.flipped
        card = self.filtered_cards[self.current_idx]
        if self.flipped:
            self.card_text.setText(f"💡 {card['a']}")
            self.card_hint.setText("Click 'Flip Card' to see the question")
            self.card_frame.setStyleSheet(f"""
                QFrame {{
                    background: {COLORS["bg_card"]};
                    border: 2px solid {COLORS["accent_green"]};
                    border-radius: 16px;
                    padding: 32px;
                    min-height: 200px;
                }}
            """)
            self.reviewed += 1
            achievement_manager.flashcards_reviewed = self.reviewed
            achievement_manager.save()
            if self.reviewed >= 20:
                achievement_manager.unlock("flashcard_20")
        else:
            self._show_card()

    def next_card(self):
        if not self.filtered_cards: return
        self.current_idx = (self.current_idx + 1) % len(self.filtered_cards)
        self._show_card()

    def prev_card(self):
        if not self.filtered_cards: return
        self.current_idx = (self.current_idx - 1) % len(self.filtered_cards)
        self._show_card()

    def shuffle_cards(self):
        if not self.filtered_cards: return
        random.shuffle(self.filtered_cards)
        self.current_idx = 0
        self._show_card()

    def filter_cards(self, category):
        if category == "All":
            self.filtered_cards = self.cards[:]
        else:
            self.filtered_cards = [c for c in self.cards if c['category'] == category]
        self.current_idx = 0
        self._show_card()


class AchievementsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(32, 24, 32, 24)
        
        title = QLabel("🏆 Achievements")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};")
        layout.addWidget(title)

        unlocked = len(achievement_manager.unlocked)
        total = len(ACHIEVEMENTS)

        summary = SectionCard("Your Progress")
        summary.add_widget(InfoLabel(f"You have unlocked {unlocked} out of {total} achievements!", True))
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(total)
        self.progress.setValue(unlocked)
        self.progress.setFormat(f"%v / %m ({unlocked*100//total}%)")
        summary.add_widget(self.progress)
        layout.addWidget(summary)

        # Grid of achievements
        grid = QGridLayout()
        grid.setSpacing(12)
        for i, (key, ach) in enumerate(ACHIEVEMENTS.items()):
            is_unlocked = key in achievement_manager.unlocked
            frame = QFrame()
            
            if is_unlocked:
                color = COLORS["accent_yellow"]
                bg_alpha = "0.15"
                icon_text = ach["icon"]
            else:
                color = COLORS["text_muted"]
                bg_alpha = "0.05"
                icon_text = "🔒"
                
            frame.setStyleSheet(f"""
                QFrame {{
                    background: rgba({QColor(color).red()},{QColor(color).green()},{QColor(color).blue()},{bg_alpha});
                    border: 1px solid {color};
                    border-radius: 10px;
                    padding: 16px;
                }}
            """)
            fl = QVBoxLayout(frame)
            
            icon_lbl = QLabel(icon_text)
            icon_lbl.setFont(QFont("Segoe UI", 28))
            icon_lbl.setAlignment(Qt.AlignCenter)
            icon_lbl.setStyleSheet("border: none;")
            fl.addWidget(icon_lbl)
            
            name_lbl = QLabel(ach["name"])
            name_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
            name_lbl.setAlignment(Qt.AlignCenter)
            name_lbl.setStyleSheet(f"color: {color}; border: none;")
            name_lbl.setWordWrap(True)
            fl.addWidget(name_lbl)
            
            desc_lbl = QLabel(ach["desc"])
            desc_lbl.setWordWrap(True)
            desc_lbl.setAlignment(Qt.AlignCenter)
            desc_lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px; border: none;")
            fl.addWidget(desc_lbl)

            row = i // 3
            col = i % 3
            grid.addWidget(frame, row, col)

        layout.addLayout(grid)
        layout.addStretch()
        
    def refresh(self):
        unlocked = len(achievement_manager.unlocked)
        total = len(ACHIEVEMENTS)
        self.progress.setMaximum(total)
        self.progress.setValue(unlocked)
        self.progress.setFormat(f"%v / %m ({unlocked*100//max(1,total)}%)")


# ─── Quiz Page (Updated for Achievements) ───────────────────────

class QuizPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.questions = self._create_questions()
        self.current_q = 0
        self.score = 0
        self.answered = False

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(32, 24, 32, 24)

        title = QLabel("🎯 Test Your Knowledge")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};")
        layout.addWidget(title)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(len(self.questions))
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.score_label = QLabel("Score: 0 / 0")
        self.score_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.score_label.setStyleSheet(f"color: {COLORS['accent_green']};")
        layout.addWidget(self.score_label)

        self.question_card = SectionCard("Question")
        self.question_label = QLabel("")
        self.question_label.setWordWrap(True)
        self.question_label.setFont(QFont("Segoe UI", 15))
        self.question_label.setStyleSheet(f"color: {COLORS['text_primary']}; padding: 12px; border: none;")
        self.question_card.add_widget(self.question_label)

        self.options_group = QButtonGroup(self)
        self.option_buttons = []
        for i in range(4):
            btn = QRadioButton()
            btn.setStyleSheet(f"""
                QRadioButton {{
                    color: {COLORS["text_secondary"]};
                    font-size: 13px;
                    padding: 8px;
                    spacing: 10px;
                }}
                QRadioButton::indicator {{
                    width: 18px;
                    height: 18px;
                }}
            """)
            self.options_group.addButton(btn, i)
            self.option_buttons.append(btn)
            self.question_card.add_widget(btn)

        self.feedback_label = QLabel("")
        self.feedback_label.setWordWrap(True)
        self.feedback_label.setFont(QFont("Segoe UI", 13))
        self.feedback_label.setStyleSheet(f"padding: 12px; border: none;")
        self.question_card.add_widget(self.feedback_label)

        btn_layout = QHBoxLayout()
        self.submit_btn = AccentButton("✅ Submit Answer", COLORS["accent_green"])
        self.submit_btn.clicked.connect(self.submit_answer)
        btn_layout.addWidget(self.submit_btn)

        self.next_btn = AccentButton("➡️ Next Question", COLORS["accent_blue"])
        self.next_btn.clicked.connect(self.next_question)
        self.next_btn.setEnabled(False)
        btn_layout.addWidget(self.next_btn)

        self.restart_btn = AccentButton("🔄 Restart Quiz", COLORS["accent_purple"])
        self.restart_btn.clicked.connect(self.restart_quiz)
        btn_layout.addWidget(self.restart_btn)

        self.question_card.add_layout(btn_layout)
        layout.addWidget(self.question_card)
        layout.addStretch()

        self._load_question()

    def _create_questions(self):
        questions = [
            {"q": "What is the complementary base pair for Adenine in DNA?", "options": ["Guanine", "Cytosine", "Thymine", "Uracil"], "answer": 2, "explanation": "In DNA, Adenine (A) always pairs with Thymine (T) through 2 hydrogen bonds."},
            {"q": "Which enzyme unwinds the DNA double helix during replication?", "options": ["DNA Polymerase", "Helicase", "Ligase", "Primase"], "answer": 1, "explanation": "Helicase breaks the hydrogen bonds between base pairs and unwinds the double helix."},
            {"q": "What type of RNA carries amino acids to the ribosome?", "options": ["mRNA", "rRNA", "tRNA", "snRNA"], "answer": 2, "explanation": "Transfer RNA (tRNA) carries specific amino acids to the ribosome."},
            {"q": "What is the start codon for translation?", "options": ["UAA", "UAG", "AUG", "UGA"], "answer": 2, "explanation": "AUG is the start codon and codes for Methionine."},
            {"q": "Which base is found in RNA but NOT in DNA?", "options": ["Adenine", "Guanine", "Cytosine", "Uracil"], "answer": 3, "explanation": "Uracil (U) replaces Thymine (T) in RNA."},
            {"q": "What type of mutation changes a codon to code for a different amino acid?", "options": ["Silent", "Missense", "Nonsense", "Frameshift"], "answer": 1, "explanation": "A missense mutation changes one amino acid to another."},
            {"q": "How many hydrogen bonds form between Guanine and Cytosine?", "options": ["1", "2", "3", "4"], "answer": 2, "explanation": "G-C base pairs have 3 hydrogen bonds, making them stronger than A-T pairs."},
            {"q": "What is the process of making mRNA from DNA called?", "options": ["Replication", "Transcription", "Translation", "Transformation"], "answer": 1, "explanation": "Transcription is the synthesis of mRNA from a DNA template."},
            {"q": "Which sugar is present in DNA nucleotides?", "options": ["Ribose", "Deoxyribose", "Glucose", "Fructose"], "answer": 1, "explanation": "DNA contains deoxyribose sugar."},
            {"q": "What happens during a nonsense mutation?", "options": ["The amino acid doesn't change", "A different amino acid is coded", "A stop codon is created", "Nucleotides are inserted/deleted"], "answer": 2, "explanation": "A nonsense mutation changes a codon to a stop codon, causing premature termination."},
            {"q": "What is the function of DNA ligase?", "options": ["Unwinds DNA", "Synthesizes RNA primers", "Joins Okazaki fragments", "Proofreads DNA"], "answer": 2, "explanation": "DNA Ligase seals nicks between Okazaki fragments."},
            {"q": "Which RNA is the most abundant in the cell?", "options": ["mRNA", "tRNA", "rRNA", "miRNA"], "answer": 2, "explanation": "rRNA makes up about 80% of total cellular RNA."},
            {"q": "What is a frameshift mutation?", "options": ["One base replaced", "Insertion/deletion not divisible by 3", "A segment inverted", "A segment moves to another chromosome"], "answer": 1, "explanation": "Frameshift mutations shift the reading frame by inserting/deleting bases not in multiples of 3."},
            {"q": "What does semi-conservative replication mean?", "options": ["Both strands are new", "Both strands are original", "Each new DNA has one old and one new strand", "Only half the DNA is replicated"], "answer": 2, "explanation": "Each daughter molecule contains one original and one newly synthesized strand."},
            {"q": "Where does transcription occur in eukaryotes?", "options": ["Cytoplasm", "Ribosome", "Nucleus", "Mitochondria"], "answer": 2, "explanation": "In eukaryotes, transcription occurs in the nucleus."},
        ]
        random.shuffle(questions)
        return questions

    def _load_question(self):
        if self.current_q >= len(self.questions):
            self._show_results()
            return
        q = self.questions[self.current_q]
        self.question_label.setText(f"Q{self.current_q + 1}: {q['q']}")
        self.feedback_label.setText("")
        self.answered = False
        self.submit_btn.setEnabled(True)
        self.next_btn.setEnabled(False)

        for i, btn in enumerate(self.option_buttons):
            btn.setChecked(False)
            btn.setEnabled(True)
            btn.setStyleSheet(f"QRadioButton {{ color: {COLORS['text_secondary']}; font-size: 13px; padding: 8px; spacing: 10px; }}")
            if i < len(q['options']):
                btn.setText(q['options'][i])
                btn.show()
            else:
                btn.hide()
        self.progress_bar.setValue(self.current_q)

    def submit_answer(self):
        selected = self.options_group.checkedId()
        if selected < 0:
            self.feedback_label.setStyleSheet(f"color: {COLORS['accent_yellow']}; padding: 12px; border: none;")
            self.feedback_label.setText("⚠️ Please select an answer first!")
            return

        self.answered = True
        q = self.questions[self.current_q]
        correct = q['answer']

        for i, btn in enumerate(self.option_buttons):
            btn.setEnabled(False)
            if i == correct:
                btn.setStyleSheet(f"QRadioButton {{ color: {COLORS['accent_green']}; font-size: 13px; font-weight: bold; padding: 8px; }}")
            elif i == selected and i != correct:
                btn.setStyleSheet(f"QRadioButton {{ color: {COLORS['accent_red']}; font-size: 13px; font-weight: bold; padding: 8px; }}")

        if selected == correct:
            self.score += 1
            achievement_manager.add_correct(1)
            self.feedback_label.setStyleSheet(f"color: {COLORS['accent_green']}; padding: 12px; border: none;")
            self.feedback_label.setText(f"✅ Correct! {q['explanation']}")
        else:
            self.feedback_label.setStyleSheet(f"color: {COLORS['accent_red']}; padding: 12px; border: none;")
            self.feedback_label.setText(f"❌ Incorrect. {q['explanation']}")

        self.score_label.setText(f"Score: {self.score} / {self.current_q + 1}")
        self.submit_btn.setEnabled(False)
        self.next_btn.setEnabled(True)

    def next_question(self):
        self.current_q += 1
        self._load_question()

    def _show_results(self):
        pct = int(self.score / len(self.questions) * 100)
        if pct >= 80:
            emoji, color, msg = "🏆", COLORS["accent_green"], "Outstanding!"
        elif pct >= 60:
            emoji, color, msg = "👍", COLORS["accent_yellow"], "Good job! Keep studying."
        else:
            emoji, color, msg = "📚", COLORS["accent_red"], "Keep learning and try again."
        
        if pct == 100:
            achievement_manager.unlock("quiz_perfect")

        self.question_label.setText(f"{emoji} Quiz Complete!\n\nScore: {self.score}/{len(self.questions)} ({pct}%)\n\n{msg}")
        self.question_label.setStyleSheet(f"color: {color}; padding: 20px; font-size: 16px; border: none;")
        self.feedback_label.setText("")
        for btn in self.option_buttons: btn.hide()
        self.submit_btn.setEnabled(False)
        self.next_btn.setEnabled(False)
        self.progress_bar.setValue(len(self.questions))

    def restart_quiz(self):
        self.questions = self._create_questions()
        self.current_q = 0
        self.score = 0
        self.score_label.setText("Score: 0 / 0")
        self.progress_bar.setValue(0)
        self.question_label.setStyleSheet(f"color: {COLORS['text_primary']}; padding: 12px; border: none;")
        for btn in self.option_buttons:
            btn.setStyleSheet(f"QRadioButton {{ color: {COLORS['text_secondary']}; font-size: 13px; padding: 8px; spacing: 10px; }}")
            btn.show()
        self._load_question()


# ─── Main Window ─────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧬 DNA & RNA Learning App - Advanced Edition")
        self.setMinimumSize(1100, 700)
        self.resize(1280, 800)
        self.setStyleSheet(STYLESHEET)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet(f"QFrame {{ background-color: {COLORS['bg_medium']}; border-right: 1px solid {COLORS['border']}; }}")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setSpacing(4)
        sidebar_layout.setContentsMargins(8, 16, 8, 16)

        app_title = QLabel("🧬 DNA & RNA")
        app_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        app_title.setStyleSheet(f"color: {COLORS['accent_cyan']}; padding: 12px 8px; border: none;")
        sidebar_layout.addWidget(app_title)

        app_subtitle = QLabel("Advanced Learning")
        app_subtitle.setFont(QFont("Segoe UI", 10))
        app_subtitle.setStyleSheet(f"color: {COLORS['text_muted']}; padding: 0px 8px 16px 8px; border: none;")
        sidebar_layout.addWidget(app_subtitle)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(f"background: {COLORS['border']}; max-height: 1px; border: none;")
        sidebar_layout.addWidget(separator)

        nav_items = [
            ("🏠 Home", "🏠", "home"),
            ("📐 DNA Structure", "📐", "dna_structure"),
            ("🔄 Replication", "🔄", "replication"),
            ("📝 Transcription", "📝", "transcription"),
            ("🏭 Translation", "🏭", "translation"),
            ("🧪 RNA Types", "🧪", "rna_types"),
            ("⚖️ DNA vs RNA", "⚖️", "comparison"),
            ("💥 Mutations", "💥", "mutations"),
            ("🎛️ Gene Regulation", "🎛️", "regulation"),
            ("🔬 Seq Analyzer", "🔬", "seq_analyzer"),
            ("🎡 Codon Wheel", "🎡", "codon_wheel"),
            ("⚡ PCR Simulator", "⚡", "pcr"),
            ("🧫 Gel Electrophoresis", "🧫", "gel"),
            ("✂️ Splicing Visualizer", "✂️", "splicing"),
            ("📜 Timeline", "📜", "timeline"),
            ("🏗️ Protein Structure", "🏗️", "protein"),
            ("🔀 Cell Division", "🔀", "cell_division"),
            ("📚 Flashcards", "📚", "flashcards"),
            ("🏆 Achievements", "🏆", "achievements"),
            ("🎯 Quiz", "🎯", "quiz"),
        ]

        self.nav_buttons = []
        self.page_map = {}
        
        # Instantiate pages
        self.pages = {
            "home": HomePage(),
            "dna_structure": DNAStructurePage(),
            "replication": ReplicationPage(),
            "transcription": TranscriptionPage(),
            "translation": TranslationPage(),
            "rna_types": RNATypesPage(),
            "comparison": DNARNAComparisonPage(),
            "mutations": MutationsPage(),
            "regulation": GeneRegulationPage(),
            "seq_analyzer": SequenceAnalyzerPage(),
            "codon_wheel": CodonWheelPage(),
            "pcr": PCRSimulatorPage(),
            "gel": GelElectrophoresisPage(),
            "splicing": SplicingVisualizerPage(),
            "timeline": TimelinePage(),
            "protein": ProteinStructurePage(),
            "cell_division": CellDivisionPage(),
            "flashcards": FlashcardPage(),
            "achievements": AchievementsPage(),
            "quiz": QuizPage(),
        }

        for text, icon, page_id in nav_items:
            btn = NavButton(text, icon)
            btn.clicked.connect(lambda checked, pid=page_id: self._switch_page(pid))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append((btn, page_id))

        sidebar_layout.addStretch()

        footer = QLabel("v2.0 — Advanced Edition")
        footer.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px; padding: 8px; border: none;")
        footer.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(footer)

        main_layout.addWidget(sidebar)

        # Pages Stack
        self.stack = QStackedWidget()
        for page_id, page_widget in self.pages.items():
            scroll = QScrollArea()
            scroll.setWidget(page_widget)
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet("border: none; background: transparent;")
            self.page_map[page_id] = self.stack.addWidget(scroll)  # index

        main_layout.addWidget(self.stack, 1)

        # Select first page & unlock first visit
        self._switch_page("home")
        achievement_manager.unlock("first_visit")

    def _switch_page(self, page_id):
        if page_id in self.page_map:
            self.stack.setCurrentIndex(self.page_map[page_id])
            for btn, pid in self.nav_buttons:
                btn.set_selected(pid == page_id)
            
            # Track page visit for achievement
            achievement_manager.visit_page(page_id)
            
            # Page-specific achievements
            if page_id == "dna_structure":
                achievement_manager.unlock("dna_structure")
            elif page_id == "replication":
                achievement_manager.unlock("replication")
            
            # Refresh dynamic pages
            if page_id == "achievements":
                self.pages["achievements"].refresh()


# ─── Entry Point ─────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    font = QFont("Segoe UI", 11)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
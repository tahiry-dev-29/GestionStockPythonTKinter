"""
Views package for GUI components and layouts
"""

from .dashboard.dashboard import DashboardWindow
from .auth.login import LoginWindow
from .auth.register import RegisterWindow

__all__ = ['DashboardWindow', 'LoginWindow', 'RegisterWindow']



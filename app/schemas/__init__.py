# app/schemas/__init__.py

# Ações
from .acoes import AcoesBase, AcoesCreate, AcoesUpdate, Acoes

# Consórcio
from .consorcio import ConsorcioBase, ConsorcioCreate, ConsorcioUpdate, Consorcio

# Equipe
from .equipe import EquipeBase, EquipeCreate, EquipeUpdate, Equipe

# Feedback
from .feedback import FeedbackBase, FeedbackCreate, FeedbackUpdate, Feedback

# Tarefas
from .tarefas import TarefasBase, TarefasCreate, TarefasUpdate, Tarefas

# TDV
from .tdv import TdvBase, TdvCreate, TdvUpdate, Tdv

__all__ = [
    "AcoesBase", "AcoesCreate", "AcoesUpdate", "Acoes",
    "ConsorcioBase", "ConsorcioCreate", "ConsorcioUpdate", "Consorcio",
    "EquipeBase", "EquipeCreate", "EquipeUpdate", "Equipe",
    "FeedbackBase", "FeedbackCreate", "FeedbackUpdate", "Feedback",
    "TarefasBase", "TarefasCreate", "TarefasUpdate", "Tarefas",
    "TdvBase", "TdvCreate", "TdvUpdate", "Tdv",
]

# app/schemas/__init__.py

# módulos completos (expõe app.schemas.esteira e app.schemas.agenda)
from . import esteira
from . import agenda

# Ações (exporta as classes individuais)
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
    # módulos
    "esteira", "agenda",
    # classes individuais
    "AcoesBase", "AcoesCreate", "AcoesUpdate", "Acoes",
    "ConsorcioBase", "ConsorcioCreate", "ConsorcioUpdate", "Consorcio",
    "EquipeBase", "EquipeCreate", "EquipeUpdate", "Equipe",
    "FeedbackBase", "FeedbackCreate", "FeedbackUpdate", "Feedback",
    "TarefasBase", "TarefasCreate", "TarefasUpdate", "Tarefas",
    "TdvBase", "TdvCreate", "TdvUpdate", "Tdv",
]

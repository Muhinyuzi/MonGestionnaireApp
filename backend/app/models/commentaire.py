from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Index, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base
from datetime import datetime



# ---------------- COMMENTAIRES ----------------
class Commentaire(Base):
    __tablename__ = "commentaires"

    id = Column(Integer, primary_key=True, index=True)
    contenu = Column(Text, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    auteur_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="CASCADE"), index=True)
    auteur = relationship("Utilisateur", back_populates="commentaires")

    tache_id = Column(Integer, ForeignKey("taches.id", ondelete="CASCADE"), index=True)
    tache = relationship("Tache", back_populates="commentaires")
 


# 🔹 Index supplémentaires pour optimiser les requêtes fréquentes
Index("idx_commentaire_auteur", Commentaire.auteur_id)
Index("idx_commentaire_note", Commentaire.tache_id)

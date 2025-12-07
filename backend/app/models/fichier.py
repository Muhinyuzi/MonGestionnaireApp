from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Index, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base
from datetime import datetime


# ---------------- FICHIERS DES NOTES ----------------
class FichierTache(Base):
    __tablename__ = "fichiers_taches"

    id = Column(Integer, primary_key=True, index=True)
    nom_fichier = Column(String(255), nullable=False)
    chemin = Column(String(255), nullable=False)

    tache_id = Column(Integer, ForeignKey("taches.id", ondelete="CASCADE"))
    tache = relationship("Tache", back_populates="fichiers")
 


# 🔹 Index supplémentaires pour optimiser les requêtes fréquentes
Index("idx_fichier_tache", FichierTache.tache_id)
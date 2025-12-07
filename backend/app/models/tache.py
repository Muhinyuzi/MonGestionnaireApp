from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base
from datetime import datetime

class Tache(Base):
    __tablename__ = "taches"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(255), nullable=False, index=True)
    contenu = Column(Text, nullable=False)
    equipe = Column(String(100), index=True)

    auteur_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="CASCADE"), index=True)
    assign_to_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=True, index=True)

    categorie = Column(String, nullable=True)
    priorite = Column(String, default="Moyenne")
    likes = Column(Integer, default=0)
    nb_vues = Column(Integer, default=0)
    resume_ia = Column(Text, nullable=True)

    # ------------------------------
    # Nouveau champ d'état
    # ------------------------------
    status = Column(String(20), default="en_attente", nullable=False)
    # valeurs possibles :
    # en_attente, active, fermee

    auteur = relationship("Utilisateur", foreign_keys=[auteur_id], back_populates="taches")
    assign_to = relationship("Utilisateur", foreign_keys=[assign_to_id], back_populates="assignations")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), index=True)

    commentaires = relationship("Commentaire", back_populates="tache", cascade="all, delete-orphan")
    fichiers = relationship("FichierTache", back_populates="tache", cascade="all, delete-orphan")


Index("idx_tache_auteur", Tache.auteur_id)
Index("idx_tache_assign_to", Tache.assign_to_id)
Index("idx_tache_equipe", Tache.equipe)

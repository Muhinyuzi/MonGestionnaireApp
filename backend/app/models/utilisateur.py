from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, Index, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base
from datetime import datetime


class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    mot_de_passe = Column(String(255), nullable=False)

    type = Column(
        String(50),
        nullable=False,
        index=True,
        server_default="user",
        doc="admin, manager, technicien, user, viewer, etc."
    )

    equipe = Column(
        String(100),
        nullable=True,
        index=True,
        server_default="Aucune"
    )

    poste = Column(String(100), nullable=True)
    telephone = Column(String(20), nullable=True)
    adresse = Column(String(255), nullable=True)
    date_embauche = Column(DateTime(timezone=True), nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    is_active = Column(Boolean, default=False)
    avatar_url = Column(String(255), nullable=True)

    # Taches créées par l'utilisateur
    taches = relationship(
        "Tache",
        back_populates="auteur",
        cascade="all, delete-orphan",
        foreign_keys="Tache.auteur_id"   # 🔥 ESSENTIEL !!!
    )

    # Notes assignées à cet utilisateur
    assignations = relationship(
        "Tache",
        back_populates="assign_to",
        foreign_keys="Tache.assign_to_id",   # 🔥 ESSENTIEL !!!
        lazy="selectin"
    )

    commentaires = relationship(
        "Commentaire",
        back_populates="auteur",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("email", name="uq_utilisateur_email"),
        Index("idx_utilisateur_nom", "nom"),
        Index("idx_utilisateur_type", "type"),
        Index("idx_utilisateur_equipe", "equipe"),
    )


import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TechnicienService, Technicien } from '../../../services/technicien.service';
import { TacheService, Tache } from '../../../services/tache.service';
import { DialogService } from '../../../services/dialog.service';
import { Location } from '@angular/common';
import { UtilisateurService } from '../../../services/utilisateur.service';

@Component({
  selector: 'app-techniciens',
  templateUrl: './techniciens.component.html',
  styleUrls: ['./techniciens.component.css']
})
export class TechniciensComponent implements OnInit {

  techniciens: Technicien[] = [];
  taches: Tache[] = [];
  isLoading = false;
  errorMessage: string = '';

  // Modale
  showTacheModal = false;
  modalTech: Technicien | null = null;
  modalMode: 'assign' | 'deassign' = 'assign';
  selectedTacheId: number | null = null;
  selectedTacheTitle: string | null = null;

  constructor(
    private api: TechnicienService,
    private userService: UtilisateurService,
    private tacheService: TacheService,
    private dialogService: DialogService,
    private location: Location,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadTechniciens();
    this.loadTaches();
  }

  loadTechniciens(): void {
    this.isLoading = true;
    this.api.getTechniciens().subscribe({
      next: (data: Technicien[]) => {
        this.techniciens = data;
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = "Erreur lors du chargement des techniciens";
        this.isLoading = false;
      }
    });
  }

  loadTaches(): void {
    this.tacheService.getTaches().subscribe({
      next: (data: { taches: Tache[] }) => this.taches = data.taches,
      error: err => console.error("Erreur chargement des tâches", err)
    });
  }

  goToDetail(tech: Technicien) {
    this.router.navigate(['/techniciens', tech.id]);
  }

  addTechnicien() {
    this.router.navigate(['/utilisateurs'], {
      queryParams: { type: 'technicien', create: true }
    });
  }

  editTechnicien(tech: Technicien) {
    this.router.navigate(['/utilisateurs'], {
      queryParams: { editId: tech.id, type: 'technicien' }
    });
  }

  deleteTechnicien(tech: Technicien) {
    this.dialogService.confirm(
      "Confirmation",
      `Voulez-vous vraiment supprimer ${tech.nom} ?`
    ).subscribe(result => {
      if (result) {
        this.userService.deleteUtilisateur(tech.id!).subscribe({
          next: () => {
            this.techniciens = this.techniciens.filter(t => t.id !== tech.id);
          },
          error: () => {
            this.dialogService.alert("Erreur", "Impossible de supprimer.");
          }
        });
      }
    });
  }

  // 🔹 Modale assignation tâche
  openAssignModal(tech: Technicien) {
    this.modalTech = tech;
    this.modalMode = 'assign';
    this.selectedTacheId = null;
    this.showTacheModal = true;
  }

  // 🔹 Modale désassignation tâche
  openDeassignModal(tech: Technicien) {
    this.modalTech = tech;
    this.modalMode = 'deassign';

    const tache = this.taches.find(t => t.id === tech.tache_id);
    this.selectedTacheTitle = tache ? tache.titre : `#${tech.tache_id}`;

    this.showTacheModal = true;
  }

  confirmTacheAction() {
    if (!this.modalTech) return;

    // ======================
    //   ASSIGNER UNE TÂCHE
    // ======================
    if (this.modalMode === 'assign') {
      if (!this.selectedTacheId) return;

      this.userService.assignTacheToUser(this.modalTech.id!, this.selectedTacheId)
        .subscribe({
          next: (updated: Technicien) => {
            const i = this.techniciens.findIndex(t => t.id === updated.id);
            if (i !== -1) this.techniciens[i] = updated;
            this.closeTacheModal();
          },
          error: err => console.error("Erreur assignation", err)
        });

      return;
    }

    // ===========================
    //   DÉSASSIGNER UNE TÂCHE
    // ===========================
    if (this.modalMode === 'deassign') {
      if (!this.modalTech.tache_id) return;

      this.userService.unassignTacheFromUser(this.modalTech.id!, this.modalTech.tache_id)
        .subscribe({
          next: (updated: Technicien) => {
            const i = this.techniciens.findIndex(t => t.id === updated.id);
            if (i !== -1) this.techniciens[i] = updated;
            this.closeTacheModal();
          },
          error: err => console.error("Erreur désassignation", err)
        });
    }
  }

  closeTacheModal() {
    this.showTacheModal = false;
    this.modalTech = null;
    this.selectedTacheId = null;
    this.selectedTacheTitle = null;
  }

  goBack(): void {
    this.location.back();
  }
}

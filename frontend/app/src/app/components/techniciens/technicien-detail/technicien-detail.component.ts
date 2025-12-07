import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { UtilisateurService, UtilisateurDetailOut } from '../../../services/utilisateur.service';

@Component({
  selector: 'app-technicien-detail',
  templateUrl: './technicien-detail.component.html',
  styleUrls: ['./technicien-detail.component.css']
})
export class TechnicienDetailComponent implements OnInit {

  technicien?: UtilisateurDetailOut;
  isLoading = true;

  // variables pour la modale
  showUnassignModal = false;
  tacheToUnassign: number | null = null;

  constructor(
    private route: ActivatedRoute,
    private userService: UtilisateurService
  ) {}

  ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.loadTechnicien(id);
  }

  loadTechnicien(id: number) {
    this.userService.getUtilisateurDetail(id).subscribe({
      next: (res) => {
        this.technicien = res;
        this.isLoading = false;
      },
      error: () => {
        this.isLoading = false;
      }
    });
  }

  // ouvre la modale avant la désassignation
  openConfirmUnassign(tacheId: number) {
    this.tacheToUnassign = tacheId;
    this.showUnassignModal = true;
  }

  closeUnassignModal() {
    this.showUnassignModal = false;
    this.tacheToUnassign = null;
  }

  confirmUnassign() {
    if (!this.tacheToUnassign || !this.technicien) return;

    // ⚠️ Le backend exige: /utilisateurs/{user_id}/unassign-tache/{tache_id}
    this.userService.unassignTacheFromUser(this.technicien.id!, this.tacheToUnassign).subscribe({
      next: () => {
        // retirer la tache de la liste affichée
        this.technicien!.assignations = 
          this.technicien!.assignations?.filter(t => t.id !== this.tacheToUnassign) ?? [];

        this.closeUnassignModal();
      },
      error: (err) => {
        console.error("Erreur lors de la désassignation", err);
      }
    });
  }
}

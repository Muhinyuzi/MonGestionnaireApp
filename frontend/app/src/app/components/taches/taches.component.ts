import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { TacheService, Tache, TacheCreate, TachesResponse } from '../../services/tache.service';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-taches',
  templateUrl: './taches.component.html',
  styleUrls: ['./taches.component.css']
})
export class TachesComponent implements OnInit {

  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;

  taches: Tache[] = [];

  newTache: TacheCreate = {
    titre: '',
    contenu: '',
    equipe: '',
    auteur_id: 0,
    categorie: '',
    priorite: ''
  };

  newFiles: File[] = [];

  page: number = 1;
  limit: number = 10;
  total: number = 0;

  searchTerm: string = '';
  selectedAuteur: string = '';
  sort: 'date_asc' | 'date_desc' = 'date_desc';

  currentUser: any = null;
  isAdmin: boolean = false;

  constructor(
    private api: TacheService,
    private auth: AuthService,
    private router: Router,
    private sanitizer: DomSanitizer
  ) {}

  sanitize(html: string): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(html);
  }

  ngOnInit(): void {
    this.currentUser = this.auth.getUser();
    this.isAdmin = this.currentUser?.type === 'admin';

    if (this.currentUser) {
      this.newTache.auteur_id = this.currentUser.id;
      this.newTache.equipe = this.currentUser.equipe;
    }

    this.loadTaches();
  }

  // ----------------------------------------------------
  // 🔍 CHARGER LES TÂCHES
  // ----------------------------------------------------
  loadTaches(): void {

    const authorFilter = this.isAdmin ? this.selectedAuteur : "";
    const assignTo = this.isAdmin ? undefined : this.currentUser?.id;

    this.api.getTaches(
      this.searchTerm,   // search
      authorFilter,      // author
      assignTo,          // assign_to (number | undefined)
      this.sort,         // sort
      this.page,         // page
      this.limit         // limit
    )
    .subscribe({
      next: (res: TachesResponse) => {
        this.taches = res.taches ?? [];
        this.total = res.total ?? 0;
      },
      error: () => {
        this.taches = [];
        this.total = 0;
      }
    });
  }

  // ----------------------------------------------------
  // 📁 GESTION DES FICHIERS
  // ----------------------------------------------------
  handleFileInput(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files) {
      this.newFiles = Array.from(input.files);
    }
  }

  removeFile(index: number): void {
    this.newFiles.splice(index, 1);
  }

  // ----------------------------------------------------
  // ➕ AJOUTER UNE TÂCHE (ADMIN ONLY)
  // ----------------------------------------------------
  addTache(): void {

    if (!this.isAdmin) {
      alert("Seul l'administrateur peut ajouter une tâche.");
      return;
    }

    if (!this.newTache.titre || !this.newTache.contenu || !this.newTache.categorie || !this.newTache.priorite) {
      alert('Veuillez remplir tous les champs obligatoires.');
      return;
    }

    this.api.createTacheWithFiles(this.newTache, this.newFiles).subscribe({
      next: (tache: Tache) => {

        this.taches.unshift(tache);

        this.newTache = {
          titre: '',
          contenu: '',
          equipe: this.currentUser?.equipe ?? '',
          auteur_id: this.currentUser?.id ?? 0,
          categorie: '',
          priorite: ''
        };

        this.newFiles = [];
        this.total += 1;

        this.router.navigate(['/taches', tache.id]);
      }
    });
  }

  // ----------------------------------------------------
  // 📄 PAGINATION
  // ----------------------------------------------------
  goToPage(page: number): void {
    if (page < 1 || page > this.totalPages) return;
    this.page = page;
    this.loadTaches();
  }

  get totalPages(): number {
    return Math.ceil(this.total / this.limit);
  }

  // ----------------------------------------------------
  // 🔧 FILTRES & TRI
  // ----------------------------------------------------
  applyFilters(): void {
    this.page = 1;
    this.loadTaches();
  }

  changeSort(sort: 'date_asc' | 'date_desc'): void {
    this.sort = sort;
    this.loadTaches();
  }
}

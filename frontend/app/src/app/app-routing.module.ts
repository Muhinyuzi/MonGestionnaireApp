import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { HomeComponent } from './components/home/home.component';

import { UtilisateursComponent } from './components/utilisateurs/utilisateurs.component';
import { UtilisateurDetailComponent } from './components/utilisateurs/utilisateur-detail/utilisateur-detail.component';

import { TachesComponent } from './components/taches/taches.component';
import { TacheCreateComponent } from './components/taches/tache-create/tache-create.component';
import { TacheDetailComponent } from './components/taches/tache-detail/tache-detail.component';


import { LoginComponent } from './components/login/login.component';
import { EmailSentComponent } from './components/pages/email-sent/email-sent.component';
import { ForgotPasswordComponent } from './components/auth/forgot-password/forgot-password.component';
import { ResetPasswordComponent } from './components/auth/reset-password/reset-password.component';
import { ActivateAccountComponent } from './components/auth/activate-account/activate-account.component';
import { ChangePasswordComponent } from './components/utilisateurs/account/change-password/change-password.component';

import { TechniciensComponent } from './components/techniciens/techniciens/techniciens.component';
import { TechnicienDetailComponent } from './components/techniciens/technicien-detail/technicien-detail.component';

import { AuthGuard } from './guards/auth.guard';
import { AdminGuard } from './guards/admin.guard';

const routes: Routes = [

  // -----------------------
  // 🔓 Routes publiques
  // -----------------------
  { path: 'login', component: LoginComponent },
  { path: 'activate', component: ActivateAccountComponent },
  { path: 'forgot-password', component: ForgotPasswordComponent },
  { path: 'reset-password', component: ResetPasswordComponent },
  { path: 'email-sent', component: EmailSentComponent },

  // -----------------------
  // 🔒 Routes protégées
  // -----------------------
  { path: '', component: HomeComponent, canActivate: [AuthGuard] },

  // --- Utilisateurs ---
  { path: 'utilisateurs', component: UtilisateursComponent, canActivate: [AuthGuard, AdminGuard] },
  { path: 'utilisateurs/:id', component: UtilisateurDetailComponent, canActivate: [AuthGuard] },
  { path: 'change-password', component: ChangePasswordComponent, canActivate: [AuthGuard] },

  // --- Techniciens (ADMIN ONLY) ---
  { path: 'techniciens', component: TechniciensComponent, canActivate: [AuthGuard, AdminGuard] },
  { path: 'techniciens/:id', component: TechnicienDetailComponent, canActivate: [AuthGuard, AdminGuard] },

  // --- TÂCHES ---
  { path: 'taches', component: TachesComponent, canActivate: [AuthGuard] },
  { path: 'taches/create', component: TacheCreateComponent, canActivate: [AuthGuard] },
  { path: 'taches/:id', component: TacheDetailComponent, canActivate: [AuthGuard] },


  // -----------------------
  // 🚨 Fallback
  // -----------------------
  { path: '**', redirectTo: 'login' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}

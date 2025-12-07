import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppComponent } from './app.component';

// -------------------- UTILISATEURS --------------------
import { UtilisateursComponent } from './components/utilisateurs/utilisateurs.component';
import { UtilisateurDetailComponent } from './components/utilisateurs/utilisateur-detail/utilisateur-detail.component';
import { ChangePasswordComponent } from './components/utilisateurs/account/change-password/change-password.component';

// -------------------- TÂCHES --------------------
import { TachesComponent } from './components/taches/taches.component';
import { TacheDetailComponent } from './components/taches/tache-detail/tache-detail.component';
import { TacheCreateComponent } from './components/taches/tache-create/tache-create.component';

// -------------------- COMMENTAIRES --------------------
import { CommentairesComponent } from './components/commentaires/commentaires.component';

// -------------------- AUTRES PAGES --------------------
import { HomeComponent } from './components/home/home.component';
import { LoginComponent } from './components/login/login.component';
import { EmailSentComponent } from './components/pages/email-sent/email-sent.component';
import { ForgotPasswordComponent } from './components/auth/forgot-password/forgot-password.component';
import { ResetPasswordComponent } from './components/auth/reset-password/reset-password.component';
import { ActivateAccountComponent } from './components/auth/activate-account/activate-account.component';


// -------------------- TECHNICIENS --------------------
import { TechniciensComponent } from './components/techniciens/techniciens/techniciens.component';
import { TechnicienDetailComponent } from './components/techniciens/technicien-detail/technicien-detail.component';

// -------------------- SHARED --------------------
import { ToastComponent } from './components/shared/toast/toast.component';
import { ConfirmDialogComponent } from './components/shared/confirm-dialog/confirm-dialog.component';

// -------------------- ROUTING --------------------
import { AppRoutingModule } from './app-routing.module';

// -------------------- ANGULAR MATERIAL --------------------
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDividerModule } from '@angular/material/divider';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';

// -------------------- WYSIWYG (Kendo Editor) --------------------
import { EditorModule } from '@progress/kendo-angular-editor';

// -------------------- AUTH INTERCEPTOR --------------------
import { AuthInterceptor } from './interceptors/auth.interceptor';

@NgModule({
  declarations: [
    AppComponent,

    // ---- Utilisateurs ----
    UtilisateursComponent,
    UtilisateurDetailComponent,
    ChangePasswordComponent,

    // ---- Tâches ----
    TachesComponent,
    TacheDetailComponent,
    TacheCreateComponent,

    // ---- Commentaires ----
    CommentairesComponent,

    // ---- Pages ----
    HomeComponent,
    LoginComponent,
    EmailSentComponent,
    ForgotPasswordComponent,
    ResetPasswordComponent,
    ActivateAccountComponent,

    // ---- Techniciens ----
    TechniciensComponent,
    TechnicienDetailComponent,

    // ---- Shared ----
    ToastComponent,
    ConfirmDialogComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    AppRoutingModule,

    // Angular Material
    BrowserAnimationsModule,
    MatDialogModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    MatFormFieldModule,
    MatInputModule,
    MatDividerModule,
    MatCardModule,
    MatIconModule,

    // Kendo Editor
    EditorModule,
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}

# 🐛 Troubleshooting: Webhook Non Ricevuto

## Problema

Il pagamento è andato a buon fine su Stripe, ma l'utente è rimasto FREE invece di diventare PRO.

## Causa

In **sviluppo locale** (`localhost:8000`), Stripe **non può inviare webhook** al tuo computer perché non è raggiungibile da internet.

Il webhook `checkout.session.completed` non è stato ricevuto, quindi il database non è stato aggiornato.

---

## ✅ Soluzione 1: Fix Immediato (Aggiornamento Manuale)

### Opzione A: Script Python

Ho creato uno script per aggiornare l'utente manualmente:

```bash
cd backend
python fix_user_plan.py tuo-email@test.com
```

Oppure per vedere gli ultimi utenti:

```bash
python fix_user_plan.py --list
```

### Opzione B: MongoDB Direttamente

Apri MongoDB Compass o la shell:

```javascript
// Trova l'utente
db.users.findOne({ email: "tuo-email@test.com" })

// Aggiorna a PRO
db.users.updateOne(
  { email: "tuo-email@test.com" },
  { 
    $set: { 
      plan: "pro",
      subscription_status: "active",
      updated_at: new Date()
    }
  }
)
```

### Opzione C: Admin Panel

1. Vai su `/admin/users`
2. Trova l'utente
3. Cambia il piano da FREE a PRO usando il dropdown

---

## 🔧 Soluzione 2: Abilitare Webhook Locali (Per il Futuro)

Per ricevere webhook in sviluppo locale, usa **Stripe CLI**:

### 1. Installa Stripe CLI

**Windows (con Scoop):**
```bash
scoop install stripe
```

**Windows (manuale):**
Scarica da: https://github.com/stripe/stripe-cli/releases

**Mac:**
```bash
brew install stripe/stripe-cli/stripe
```

### 2. Login a Stripe

```bash
stripe login
```

Segui le istruzioni per autenticarti.

### 3. Inoltra Webhook al Backend Locale

```bash
stripe listen --forward-to localhost:8000/payment/webhook
```

Dovresti vedere:
```
> Ready! Your webhook signing secret is whsec_xxxxxxxxxxxxx
```

### 4. Copia il Webhook Secret

Copia il `whsec_xxxxxxxxxxxxx` e aggiungilo in:
- `/admin/settings` → Stripe Webhook Secret

### 5. Testa di Nuovo

Ora quando fai un pagamento test, il webhook verrà inoltrato al tuo backend locale e l'utente verrà aggiornato automaticamente!

---

## 🧪 Test con Stripe CLI

Puoi anche simulare eventi senza fare pagamenti reali:

```bash
# Simula checkout completato
stripe trigger checkout.session.completed

# Simula cancellazione abbonamento
stripe trigger customer.subscription.deleted
```

---

## 📝 Note per Produzione

In **produzione**, i webhook funzioneranno automaticamente perché il tuo server sarà raggiungibile da internet.

Dovrai solo:
1. Configurare il webhook endpoint su Stripe Dashboard
2. URL: `https://tuo-dominio.com/payment/webhook`
3. Eventi: `checkout.session.completed`, `customer.subscription.deleted`, `customer.subscription.updated`
4. Copiare il signing secret nelle impostazioni admin

---

## ✅ Riepilogo

**Per ora:**
- Usa lo script `fix_user_plan.py` o l'admin panel per aggiornare l'utente a PRO

**Per il futuro:**
- Installa Stripe CLI
- Usa `stripe listen --forward-to localhost:8000/payment/webhook`
- Copia il webhook secret nelle impostazioni admin

**In produzione:**
- I webhook funzioneranno automaticamente! 🎉

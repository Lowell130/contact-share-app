# 📇 ContactShare - Digital Business Card Platform

> **Your business card, reinvented.** Create, customize, and share your professional identity in seconds. Sustainable, smart, and always up-to-date.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 🌟 Overview

ContactShare is a modern, full-stack web application that allows users to create and share digital business cards. Say goodbye to paper cards that end up in the trash - with ContactShare, your professional identity is always with you, on your smartphone, ready to be shared instantly via QR codes, direct links, or social media.

### ✨ Key Features

- 🎨 **Multiple Premium Themes** - Choose from minimal, gradient, dark, flowbite, and modern color variants (Emerald, Blue, Indigo, Rose, Orange)
- 📊 **Advanced Analytics** - Track card views, vCard downloads, referrers, devices, geographic data, and social clicks
- 🔗 **Flexible Sharing** - Share via QR codes, direct links, email, WhatsApp, or temporary password-protected links
- 👤 **Custom Avatars** - Upload your own avatar or use auto-generated ones
- 🔒 **Privacy Controls** - Control card visibility and search engine indexing
- 💳 **Stripe Integration** - Pro plan subscription with premium features (€4.99/mo)
- 📱 **Fully Responsive** - Beautiful UI that works seamlessly on desktop, tablet, and mobile
- 🌐 **SEO Optimized** - Proper meta tags and indexing controls for public cards
- 🔐 **Secure Authentication** - JWT-based auth with refresh tokens and magic link support
- ⚡ **Rate Limiting** - Built-in API rate limiting for security

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern, fast Python web framework
- **MongoDB** - NoSQL database with Motor async driver
- **Pydantic** - Data validation and settings management
- **JWT** - Secure token-based authentication
- **Stripe** - Payment processing
- **Pillow & QRCode** - Image processing and QR code generation
- **SlowAPI** - Rate limiting middleware

### Frontend
- **Nuxt 3** - Vue.js framework for production
- **Vue 3** - Progressive JavaScript framework
- **TailwindCSS 4** - Utility-first CSS framework
- **Flowbite** - UI component library
- **ApexCharts** - Interactive charts for analytics

## 📁 Project Structure

```
contact-share-app/
├── backend/
│   ├── app/
│   │   ├── routers/          # API endpoints
│   │   │   ├── auth.py       # Authentication (register, login, magic link)
│   │   │   ├── cards.py      # Card CRUD operations
│   │   │   ├── public.py     # Public card views & vCard download
│   │   │   ├── analytics.py  # Analytics tracking & reporting
│   │   │   ├── share.py      # Temporary share links
│   │   │   ├── payment.py    # Stripe integration
│   │   │   ├── admin.py      # Admin operations
│   │   │   └── me.py         # User profile
│   │   ├── services/         # Business logic
│   │   ├── models.py         # Pydantic models
│   │   ├── config.py         # Configuration settings
│   │   ├── db.py             # Database connection
│   │   ├── security.py       # Auth utilities
│   │   ├── deps.py           # FastAPI dependencies
│   │   ├── limiter.py        # Rate limiting
│   │   └── main.py           # Application entry point
│   ├── static/               # Static files (avatars, QR codes)
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── pages/                # Nuxt pages
│   │   ├── index.vue         # Landing page
│   │   ├── login.vue         # Login page
│   │   ├── register.vue      # Registration page
│   │   ├── dashboard.vue     # User dashboard
│   │   ├── account.vue       # Account settings
│   │   ├── upgrade.vue       # Subscription upgrade
│   │   ├── cards/            # Card management
│   │   ├── analytics/        # Analytics views
│   │   ├── admin/            # Admin panel
│   │   └── c/                # Public card view
│   ├── components/           # Vue components
│   │   ├── AppHeader.vue     # Navigation header
│   │   ├── AppFooter.vue     # Footer
│   │   ├── CardForm.vue      # Card creation/editing form
│   │   ├── PublicCard*.vue   # Card theme templates
│   │   └── PublicSocialList.vue # Social media links
│   ├── composables/          # Vue composables
│   ├── middleware/           # Route middleware
│   ├── layouts/              # Page layouts
│   └── nuxt.config.ts        # Nuxt configuration
└── postman/                  # API testing collection

```

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+**
- **Node.js 18+** and npm
- **MongoDB** (local or cloud instance)
- **Stripe Account** (for payment features)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file:**
   ```env
   # Database
   MONGO_URI=mongodb://localhost:27017
   MONGO_DB=contact_share

   # Authentication
   JWT_SECRET=your-secret-key-here
   JWT_REFRESH_SECRET=your-refresh-secret-here
   MAGIC_TOKEN_SECRET=your-magic-secret-here
   ACCESS_EXPIRES_MIN=30
   REFRESH_EXPIRES_DAYS=14

   # Application
   BASE_URL=http://localhost:8000
   FRONTEND_URL=http://localhost:3000

   # CORS (comma-separated or JSON array)
   CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
   CORS_ORIGIN_REGEX=https?://(localhost|127\.0\.0\.1)(:\d+)?$

   # Stripe (optional, for payments)
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_PRICE_ID=price_...
   ```

5. **Run the backend:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000`
   - API docs: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create `.env` file (if needed):**
   ```env
   NUXT_PUBLIC_API_BASE=http://localhost:8000
   ```

4. **Run the development server:**
   ```bash
   npm run dev
   ```

   The application will be available at `http://localhost:3000`

## 📖 Usage

### Creating Your First Card

1. **Register** for a free account at `/register`
2. **Login** to access your dashboard
3. **Create a card** by clicking "Create New Card"
4. **Customize** your card:
   - Add title and custom slug
   - Upload avatar or use auto-generated one
   - Add contact fields (email, phone, website, social media, etc.)
   - Choose a theme (free or premium)
   - Configure privacy settings
5. **Share** your card via:
   - QR code (download or display)
   - Direct link (`/c/your-slug`)
   - Temporary share link with optional password
   - Social media or email

### Analytics

Track your card's performance:
- **Total views** and vCard downloads
- **24-hour** and **7-day** view counts
- **30-day trend** visualization
- **Top referrers** - See where your traffic comes from
- **Device breakdown** - Mobile, desktop, tablet, other
- **Geographic data** - Top countries viewing your card
- **Social clicks** - Track clicks on social media links

### Upgrading to Pro

Unlock premium features for €4.99/month:
- ✨ Premium "Modern" themes with custom colors
- 📊 Advanced analytics (coming soon)
- ✓ Verified badge (coming soon)

## 🔌 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login with email/password
- `POST /auth/refresh` - Refresh access token
- `POST /auth/magic/request` - Request magic link
- `POST /auth/magic/confirm` - Confirm magic link
- `DELETE /auth/me` - Delete account

### Cards (Protected)
- `GET /cards` - List user's cards
- `POST /cards` - Create new card
- `GET /cards/{id}` - Get card details
- `PUT /cards/{id}` - Update card
- `DELETE /cards/{id}` - Delete card

### Public
- `GET /public/cards/{slug}` - View public card
- `GET /public/cards/{slug}/vcard` - Download vCard
- `POST /public/track` - Track analytics event

### Analytics
- `GET /analytics/{card_id}` - Get card analytics

### Sharing
- `POST /share` - Create temporary share link
- `GET /share/{slug}` - Access shared card

### Payment
- `POST /payment/create-checkout` - Create Stripe checkout session
- `POST /payment/webhook` - Stripe webhook handler

### Admin
- `GET /admin/stats` - Platform statistics (admin only)

## 🎨 Available Themes

### Free Themes
- **Minimal** - Clean and simple design
- **Gradient** - Colorful gradient background
- **Dark** - Dark mode theme
- **Flowbite** - Modern Flowbite-based design

### Pro Themes (Premium)
- **Modern Emerald** - Vibrant emerald green
- **Modern Blue** - Professional blue
- **Modern Indigo** - Deep indigo
- **Modern Rose** - Elegant rose
- **Modern Orange** - Energetic orange

## 🔒 Security Features

- **JWT Authentication** with access and refresh tokens
- **Password hashing** using bcrypt
- **Rate limiting** on API endpoints
- **CORS protection** with configurable origins
- **Input validation** with Pydantic models
- **Secure file uploads** with type validation

## 📊 Database Schema

### Users Collection
```javascript
{
  _id: ObjectId,
  email: String (unique),
  password_hash: String (nullable),
  name: String,
  plan: String ("free" | "pro"),
  stripe_customer_id: String (optional),
  stripe_subscription_id: String (optional),
  created_at: DateTime
}
```

### Cards Collection
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  title: String,
  slug: String (unique),
  fields: Array<{type, label, value, visible}>,
  theme: String,
  avatar_url: String,
  is_public: Boolean,
  is_indexed: Boolean,
  allow_vcard: Boolean,
  notes: String,
  created_at: DateTime,
  updated_at: DateTime
}
```

### Analytics Collection
```javascript
{
  _id: ObjectId,
  card_id: ObjectId,
  event_type: String ("view" | "vcard" | "social_click"),
  timestamp: DateTime,
  referrer: String,
  device: String,
  country: String,
  social_platform: String (optional)
}
```

## 🧪 Testing

### Using Postman

A Postman collection is included in the `postman/` directory:
- `contact-share.postman_collection.json` - API endpoints
- `contact-share.postman_environment.json` - Environment variables

Import both files into Postman to test the API.

### Manual Testing

1. Start both backend and frontend
2. Register a new account
3. Create a card with various fields
4. Test public card view at `/c/your-slug`
5. Download vCard and import to contacts
6. Check analytics dashboard

## 🚢 Deployment

### Backend Deployment (Google Cloud Run / Heroku / Railway)

1. Set environment variables in your platform
2. Ensure MongoDB is accessible (use MongoDB Atlas for cloud)
3. Configure CORS origins to include your production frontend URL
4. Set up Stripe webhook endpoint for production

### Frontend Deployment (Vercel / Netlify)

1. Build the application:
   ```bash
   npm run build
   ```

2. Set environment variables:
   ```env
   NUXT_PUBLIC_API_BASE=https://your-api-domain.com
   ```

3. Deploy the `.output` directory

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** - For the amazing Python web framework
- **Nuxt.js** - For the powerful Vue.js framework
- **TailwindCSS** - For the utility-first CSS framework
- **Flowbite** - For the beautiful UI components
- **Stripe** - For seamless payment processing
- **MongoDB** - For the flexible NoSQL database

## 📧 Contact & Support

For questions, issues, or feature requests, please open an issue on GitHub.

---

**Made with ❤️ by ContactShare Team**

*Sustainable networking for the modern professional.*

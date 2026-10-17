
import { useEffect, useState } from 'react'
import './App.css'

const API_URL = '/api/events/'

const categories = [
  'همه رویدادها',
  'فناوری',
  'آموزشی',
  'کسب‌وکار',
  'هنر',
]

const nextStatus = {
  draft: 'published',
  published: 'closed',
  closed: 'finished',
}

const statusLabels = {
  draft: 'پیش‌نویس',
  published: 'منتشرشده',
  closed: 'بسته‌شده',
  finished: 'پایان‌یافته',
}

function getErrorMessage(data, fallback) {
  if (data?.detail) {
    return data.detail
  }

  if (data && typeof data === 'object') {
    return Object.entries(data)
      .map(([key, value]) => {
        const message = Array.isArray(value)
          ? value.join(' ')
          : String(value)

        return `${key}: ${message}`
      })
      .join(' | ') || fallback
  }

  return fallback
}

function App() {
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [search, setSearch] = useState('')
  const [activeCategory, setActiveCategory] = useState('همه رویدادها')

  const [selectedEvent, setSelectedEvent] = useState(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [detailError, setDetailError] = useState('')

  const [authMode, setAuthMode] = useState('login')
  const [showAuth, setShowAuth] = useState(false)
  const [authLoading, setAuthLoading] = useState(false)
  const [authError, setAuthError] = useState('')
  const [authSuccess, setAuthSuccess] = useState('')
  const [currentUser, setCurrentUser] = useState(null)

  const [authForm, setAuthForm] = useState({
    username: '',
    email: '',
    password: '',
    role: 'participant',
  })

  const [showOrganizerPanel, setShowOrganizerPanel] = useState(false)
  const [organizerEvents, setOrganizerEvents] = useState([])
  const [organizerLoading, setOrganizerLoading] = useState(false)
  const [organizerError, setOrganizerError] = useState('')
  const [organizerSuccess, setOrganizerSuccess] = useState('')

  const [eventForm, setEventForm] = useState({
    title: '',
    description: '',
    start_at: '',
    end_at: '',
    capacity: 30,
  })

  useEffect(() => {
    const token = localStorage.getItem('eventPlanetToken')

    if (!token) {
      return
    }

    fetch('/api/accounts/profile/', {
      headers: {
        Authorization: `Token ${token}`,
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('نشست معتبر نیست')
        }

        return response.json()
      })
      .then((user) => {
        setCurrentUser(user)
      })
      .catch(() => {
        localStorage.removeItem('eventPlanetToken')
        setCurrentUser(null)
      })
  }, [])

  useEffect(() => {
    const controller = new AbortController()

    async function fetchEvents() {
      try {
        const response = await fetch(API_URL, {
          signal: controller.signal,
        })

        if (!response.ok) {
          throw new Error(`خطای سرور: ${response.status}`)
        }

        const data = await response.json()
        const items = Array.isArray(data) ? data : data.results

        if (!Array.isArray(items)) {
          throw new Error('ساختار پاسخ API معتبر نیست.')
        }

        setEvents(items)
        setError('')
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(
            'دریافت رویدادها انجام نشد. اتصال به API را بررسی کن.',
          )
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false)
        }
      }
    }

    fetchEvents()

    return () => controller.abort()
  }, [])

  function handleLogout() {
    localStorage.removeItem('eventPlanetToken')
    setCurrentUser(null)
    setShowOrganizerPanel(false)
    setOrganizerEvents([])
    setShowAuth(false)
    setAuthSuccess('با موفقیت از حساب کاربری خارج شدی.')
  }

  async function handleAuthSubmit(event) {
    event.preventDefault()
    setAuthError('')
    setAuthSuccess('')
    setAuthLoading(true)

    const isRegister = authMode === 'register'

    const endpoint = isRegister
      ? '/api/accounts/register/'
      : '/api/accounts/login/'

    const payload = isRegister
      ? authForm
      : {
          username: authForm.username,
          password: authForm.password,
        }

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          getErrorMessage(data, 'اطلاعات واردشده معتبر نیست.'),
        )
      }

      if (isRegister) {
        setAuthSuccess('ثبت‌نام موفق بود. حالا وارد حساب کاربری شو.')
        setAuthMode('login')
        setAuthForm((previous) => ({
          ...previous,
          password: '',
        }))
      } else {
        localStorage.setItem('eventPlanetToken', data.token)

        setCurrentUser({
          id: data.user_id,
          username: data.username,
          role: data.role,
        })

        setAuthSuccess(`خوش آمدی ${data.username}!`)
        setShowAuth(false)
        setAuthForm({
          username: '',
          email: '',
          password: '',
          role: 'participant',
        })
      }
    } catch (err) {
      setAuthError(err.message || 'ارتباط با سرور برقرار نشد.')
    } finally {
      setAuthLoading(false)
    }
  }

  async function openEventDetails(eventId) {
    setSelectedEvent(null)
    setDetailError('')
    setDetailLoading(true)

    try {
      const response = await fetch(`${API_URL}${eventId}/`)

      if (!response.ok) {
        throw new Error(`خطای سرور: ${response.status}`)
      }

      const data = await response.json()
      setSelectedEvent(data)
    } catch {
      setDetailError('دریافت جزئیات رویداد انجام نشد. دوباره تلاش کن.')
    } finally {
      setDetailLoading(false)
    }
  }

  async function loadOrganizerEvents() {
    const token = localStorage.getItem('eventPlanetToken')

    if (!token) {
      setOrganizerError('ابتدا وارد حساب کاربری شو.')
      return
    }

    setOrganizerLoading(true)
    setOrganizerError('')

    try {
      const response = await fetch('/api/organizer/events/', {
        headers: {
          Authorization: `Token ${token}`,
        },
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          getErrorMessage(data, 'دریافت رویدادهای برگزارکننده انجام نشد.'),
        )
      }

      const items = Array.isArray(data) ? data : data.results

      if (!Array.isArray(items)) {
        throw new Error('ساختار فهرست رویدادها معتبر نیست.')
      }

      setOrganizerEvents(items)
    } catch (err) {
      setOrganizerError(err.message || 'خطا در ارتباط با سرور.')
    } finally {
      setOrganizerLoading(false)
    }
  }

  async function handleCreateEvent(event) {
    event.preventDefault()
    setOrganizerError('')
    setOrganizerSuccess('')

    const token = localStorage.getItem('eventPlanetToken')

    if (!token) {
      setOrganizerError('ابتدا وارد حساب کاربری شو.')
      return
    }

    if (
      new Date(eventForm.end_at) <=
      new Date(eventForm.start_at)
    ) {
      setOrganizerError('زمان پایان باید بعد از زمان شروع باشد.')
      return
    }

    setOrganizerLoading(true)

    try {
      const response = await fetch('/api/organizer/events/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify({
          ...eventForm,
          capacity: Number(eventForm.capacity),
          start_at: new Date(eventForm.start_at).toISOString(),
          end_at: new Date(eventForm.end_at).toISOString(),
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          getErrorMessage(data, 'ساخت رویداد انجام نشد.'),
        )
      }

      setOrganizerSuccess('رویداد با موفقیت ساخته شد.')

      setEventForm({
        title: '',
        description: '',
        start_at: '',
        end_at: '',
        capacity: 30,
      })

      await loadOrganizerEvents()
    } catch (err) {
      setOrganizerError(err.message || 'خطا در ساخت رویداد.')
    } finally {
      setOrganizerLoading(false)
    }
  }

  async function handleEventStatus(eventId, newStatus) {
    setOrganizerError('')
    setOrganizerSuccess('')

    const token = localStorage.getItem('eventPlanetToken')

    if (!token) {
      setOrganizerError('ابتدا وارد حساب کاربری شو.')
      return
    }

    setOrganizerLoading(true)

    try {
      const response = await fetch(
        `/api/organizer/events/${eventId}/status/`,
        {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${token}`,
          },
          body: JSON.stringify({
            status: newStatus,
          }),
        },
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          getErrorMessage(data, 'تغییر وضعیت رویداد انجام نشد.'),
        )
      }

      setOrganizerSuccess(
        `وضعیت رویداد به «${statusLabels[newStatus]}» تغییر کرد.`,
      )

      await loadOrganizerEvents()
    } catch (err) {
      setOrganizerError(err.message || 'خطا در تغییر وضعیت رویداد.')
    } finally {
      setOrganizerLoading(false)
    }
  }

  const filteredEvents = events.filter((event) => {
    const title = String(event.title ?? '').toLowerCase()
    const description = String(event.description ?? '').toLowerCase()
    const query = search.trim().toLowerCase()

    return title.includes(query) || description.includes(query)
  })

  return (
    <div className="app" dir="rtl">
      <header className="navbar">
        <a className="brand" href="/" aria-label="صفحه اصلی ایونت پلنت">
          <span className="brand-icon">E</span>
          <span>
            EVENT <strong>PLANET</strong>
          </span>
        </a>

        <nav className="nav-links">
          <a className="active" href="#home">
            صفحه اصلی
          </a>
          <a href="#events">
            رویدادها
          </a>
          <a href="#about">
            درباره ما
          </a>
        </nav>

        {currentUser ? (
          <div className="user-menu">
            <span className="user-greeting">
              {currentUser.username}
            </span>

            {currentUser.role === 'organizer' && (
              <button
                className="login-button"
                type="button"
                onClick={() => {
                  const willOpen = !showOrganizerPanel

                  setShowOrganizerPanel(willOpen)
                  setOrganizerError('')
                  setOrganizerSuccess('')

                  if (willOpen) {
                    loadOrganizerEvents()
                  }
                }}
              >
                {showOrganizerPanel ? 'بستن پنل' : 'پنل برگزارکننده'}
              </button>
            )}

            <button
              className="login-button"
              type="button"
              onClick={handleLogout}
            >
              خروج
            </button>
          </div>
        ) : (
          <button
            className="login-button"
            type="button"
            onClick={() => {
              setShowAuth(true)
              setAuthMode('login')
              setAuthError('')
              setAuthSuccess('')
            }}
          >
            ورود / ثبت‌نام
          </button>
        )}
      </header>

      {authSuccess && (
        <div className="auth-notice">{authSuccess}</div>
      )}

      {showAuth && (
        <section className="auth-section" id="login">
          <div className="auth-card">
            <button
              className="details-button"
              type="button"
              onClick={() => setShowAuth(false)}
            >
              بستن ×
            </button>

            <span className="eyebrow">
              به EVENT PLANET خوش آمدی
            </span>

            <h2>
              {authMode === 'login'
                ? 'ورود به حساب کاربری'
                : 'ساخت حساب کاربری'}
            </h2>

            <p>
              {authMode === 'login'
                ? 'برای ادامه وارد حساب خودت شو.'
                : 'اطلاعاتت را وارد کن و نقش خودت را انتخاب کن.'}
            </p>

            <div className="auth-tabs">
              <button
                type="button"
                className={
                  authMode === 'login'
                    ? 'category active'
                    : 'category'
                }
                onClick={() => {
                  setAuthMode('login')
                  setAuthError('')
                  setAuthSuccess('')
                }}
              >
                ورود
              </button>

              <button
                type="button"
                className={
                  authMode === 'register'
                    ? 'category active'
                    : 'category'
                }
                onClick={() => {
                  setAuthMode('register')
                  setAuthError('')
                  setAuthSuccess('')
                }}
              >
                ثبت‌نام
              </button>
            </div>

            <form
              onSubmit={handleAuthSubmit}
              className="auth-form"
            >
              <label>
                نام کاربری
                <input
                  required
                  autoComplete="username"
                  value={authForm.username}
                  onChange={(event) =>
                    setAuthForm({
                      ...authForm,
                      username: event.target.value,
                    })
                  }
                />
              </label>

              {authMode === 'register' && (
                <>
                  <label>
                    ایمیل
                    <input
                      required
                      type="email"
                      autoComplete="email"
                      value={authForm.email}
                      onChange={(event) =>
                        setAuthForm({
                          ...authForm,
                          email: event.target.value,
                        })
                      }
                    />
                  </label>

                  <label>
                    نقش کاربری
                    <select
                      value={authForm.role}
                      onChange={(event) =>
                        setAuthForm({
                          ...authForm,
                          role: event.target.value,
                        })
                      }
                    >
                      <option value="participant">
                        شرکت‌کننده
                      </option>
                      <option value="organizer">
                        برگزارکننده
                      </option>
                    </select>
                  </label>
                </>
              )}

              <label>
                رمز عبور
                <input
                  required
                  type="password"
                  minLength={authMode === 'register' ? 8 : undefined}
                  autoComplete={
                    authMode === 'login'
                      ? 'current-password'
                      : 'new-password'
                  }
                  value={authForm.password}
                  onChange={(event) =>
                    setAuthForm({
                      ...authForm,
                      password: event.target.value,
                    })
                  }
                />
              </label>

              {authError && (
                <p className="error-message" role="alert">
                  {authError}
                </p>
              )}

              <button
                className="primary-button auth-submit"
                type="submit"
                disabled={authLoading}
              >
                {authLoading
                  ? 'لطفاً صبر کن...'
                  : authMode === 'login'
                    ? 'ورود به حساب'
                    : 'ثبت‌نام'}
              </button>
            </form>
          </div>
        </section>
      )}

      {showOrganizerPanel && currentUser?.role === 'organizer' && (
        <section className="auth-section organizer-panel">
          <div className="auth-card organizer-card">
            <span className="eyebrow">مدیریت رویدادها</span>
            <h2>پنل برگزارکننده</h2>
            <p>رویداد جدید بساز و رویدادهای خودت را مدیریت کن.</p>

            {organizerError && (
              <p className="error-message" role="alert">
                {organizerError}
              </p>
            )}

            {organizerSuccess && (
              <p className="auth-notice">
                {organizerSuccess}
              </p>
            )}

            <form
              className="auth-form"
              onSubmit={handleCreateEvent}
            >
              <label>
                عنوان رویداد
                <input
                  required
                  value={eventForm.title}
                  onChange={(event) =>
                    setEventForm({
                      ...eventForm,
                      title: event.target.value,
                    })
                  }
                  placeholder="مثلاً کارگاه آموزش پایتون"
                />
              </label>

              <label>
                توضیحات
                <textarea
                  required
                  rows="4"
                  value={eventForm.description}
                  onChange={(event) =>
                    setEventForm({
                      ...eventForm,
                      description: event.target.value,
                    })
                  }
                  placeholder="درباره رویداد توضیح بده..."
                />
              </label>

              <label>
                زمان شروع
                <input
                  required
                  type="datetime-local"
                  value={eventForm.start_at}
                  onChange={(event) =>
                    setEventForm({
                      ...eventForm,
                      start_at: event.target.value,
                    })
                  }
                />
              </label>

              <label>
                زمان پایان
                <input
                  required
                  type="datetime-local"
                  min={eventForm.start_at || undefined}
                  value={eventForm.end_at}
                  onChange={(event) =>
                    setEventForm({
                      ...eventForm,
                      end_at: event.target.value,
                    })
                  }
                />
              </label>

              <label>
                ظرفیت شرکت‌کنندگان
                <input
                  required
                  type="number"
                  min="1"
                  value={eventForm.capacity}
                  onChange={(event) =>
                    setEventForm({
                      ...eventForm,
                      capacity: event.target.value,
                    })
                  }
                />
              </label>

              <button
                className="primary-button auth-submit"
                type="submit"
                disabled={organizerLoading}
              >
                {organizerLoading
                  ? 'در حال پردازش...'
                  : 'ساخت رویداد'}
              </button>
            </form>

            <div className="organizer-events">
              <h3>رویدادهای من</h3>

              {organizerLoading && (
                <p>در حال دریافت اطلاعات...</p>
              )}

              {!organizerLoading &&
                organizerEvents.length === 0 && (
                  <p>هنوز رویدادی نساخته‌ای.</p>
                )}

              {organizerEvents.map((event) => (
                <article
                  className="organizer-event-item"
                  key={event.id}
                >
                  <strong>{event.title}</strong>

                  <span>
                    وضعیت: {statusLabels[event.status] || event.status}
                  </span>

                  <span>ظرفیت: {event.capacity}</span>

                  {nextStatus[event.status] && (
                    <button
                      className="details-button"
                      type="button"
                      disabled={organizerLoading}
                      onClick={() =>
                        handleEventStatus(
                          event.id,
                          nextStatus[event.status],
                        )
                      }
                    >
                      {event.status === 'draft'
                        ? 'انتشار رویداد'
                        : event.status === 'published'
                          ? 'بستن ثبت‌نام'
                          : 'پایان‌دادن به رویداد'}
                    </button>
                  )}
                </article>
              ))}
            </div>
          </div>
        </section>
      )}

      <main>
        {!selectedEvent && (
          <section className="hero" id="home">
            <div className="hero-content">
              <span className="eyebrow">
                دنیایی از تجربه‌های تازه
              </span>

              <h1>
                رویداد بعدی تو
                <br />
                <span>اینجا شروع می‌شه!</span>
              </h1>

              <p>
                رویدادهای جذاب را کشف کن، چیزهای تازه یاد بگیر
                و با آدم‌های هم‌علاقه خودت آشنا شو.
              </p>

              <a className="primary-button" href="#events">
                کشف رویدادها <span aria-hidden="true">←</span>
              </a>

              <div className="hero-stats">
                <div>
                  <strong>{events.length}</strong>
                  <span>رویداد دریافت‌شده</span>
                </div>
                <div>
                  <strong>۲۴/۷</strong>
                  <span>دسترسی آنلاین</span>
                </div>
                <div>
                  <strong>∞</strong>
                  <span>فرصت یادگیری</span>
                </div>
              </div>
            </div>

            <div className="hero-art" aria-hidden="true">
              <div className="orbit orbit-one"></div>
              <div className="orbit orbit-two"></div>
              <div className="planet">
                <span>EP</span>
              </div>
              <div className="floating-card card-top">
                ✦ تجربه‌های جدید
              </div>
              <div className="floating-card card-bottom">
                ↗ مسیر پیشرفت تو
              </div>
            </div>
          </section>
        )}

        {detailLoading && (
          <section className="events-section">
            <p className="message">
              در حال دریافت جزئیات رویداد...
            </p>
          </section>
        )}

        {detailError && (
          <section className="events-section">
            <div className="message error-message">
              <p>{detailError}</p>
              <button
                type="button"
                onClick={() => window.location.reload()}
              >
                تلاش دوباره
              </button>
            </div>
          </section>
        )}

        {selectedEvent && (
          <section
            className="events-section event-details"
            id="event-details"
          >
            <button
              className="details-button"
              type="button"
              onClick={() => setSelectedEvent(null)}
            >
              ← بازگشت به رویدادها
            </button>

            <span className="eyebrow">جزئیات رویداد</span>
            <h2>{selectedEvent.title}</h2>

            <p className="event-description">
              {selectedEvent.description ||
                'توضیحی برای این رویداد ثبت نشده است.'}
            </p>

            <div className="event-meta">
              <span>
                وضعیت:{' '}
                {statusLabels[selectedEvent.status] ||
                  selectedEvent.status ||
                  'اعلام نشده'}
              </span>

              <span>
                ظرفیت: {selectedEvent.capacity ?? 'اعلام نشده'}
              </span>

              <span>
                زمان شروع:{' '}
                {selectedEvent.start_at
                  ? new Date(selectedEvent.start_at).toLocaleString(
                      'fa-IR',
                    )
                  : 'اعلام نشده'}
              </span>

              <span>
                زمان پایان:{' '}
                {selectedEvent.end_at
                  ? new Date(selectedEvent.end_at).toLocaleString(
                      'fa-IR',
                    )
                  : 'اعلام نشده'}
              </span>
            </div>
          </section>
        )}

        {!selectedEvent && (
          <section className="events-section" id="events">
            <div className="section-heading">
              <div>
                <span className="eyebrow">انتخاب با توست</span>
                <h2>رویدادهای پیش رو</h2>
                <p>رویدادی متناسب با علاقه‌ات پیدا کن.</p>
              </div>

              <span className="event-count">
                {events.length} رویداد
              </span>
            </div>

            <label className="search-box">
              <span aria-hidden="true">⌕</span>
              <input
                type="search"
                placeholder="نام یا توضیحات رویداد را جست‌وجو کن..."
                value={search}
                onChange={(event) => setSearch(event.target.value)}
              />
            </label>

            <div className="categories" aria-label="دسته‌بندی رویدادها">
              {categories.map((category) => (
                <button
                  key={category}
                  className={
                    activeCategory === category
                      ? 'category active'
                      : 'category'
                  }
                  onClick={() => setActiveCategory(category)}
                  type="button"
                >
                  {category}
                </button>
              ))}
            </div>

            {loading && (
              <p className="message">
                در حال دریافت رویدادها...
              </p>
            )}

            {!loading && error && (
              <div className="message error-message">
                <p>{error}</p>
                <button
                  type="button"
                  onClick={() => window.location.reload()}
                >
                  تلاش دوباره
                </button>
              </div>
            )}

            {!loading && !error && filteredEvents.length === 0 && (
              <div className="message">
                هنوز رویدادی برای نمایش پیدا نشد.
              </div>
            )}

            {!loading && !error && filteredEvents.length > 0 && (
              <div className="events-grid">
                {filteredEvents.map((event) => (
                  <article className="event-card" key={event.id}>
                    <div className="event-cover">
                      <span className="event-symbol">✦</span>
                      <span className="status-badge">
                        {event.status === 'published'
                          ? 'در حال ثبت‌نام'
                          : statusLabels[event.status] ||
                            event.status ||
                            'رویداد'}
                      </span>
                    </div>

                    <div className="event-body">
                      <span className="event-category">
                        رویداد ویژه
                      </span>

                      <h3>{event.title}</h3>

                      <p className="event-description">
                        {event.description ||
                          'برای آشنایی با جزئیات این رویداد، ادامه مسیر را دنبال کن.'}
                      </p>

                      <div className="event-meta">
                        <span>
                          ◷{' '}
                          {event.start_at
                            ? new Date(
                                event.start_at,
                              ).toLocaleDateString('fa-IR')
                            : 'تاریخ اعلام نشده'}
                        </span>

                        <span>
                          ♙ ظرفیت: {event.capacity ?? 'اعلام نشده'}
                        </span>
                      </div>

                      <button
                        className="details-button"
                        type="button"
                        onClick={() => openEventDetails(event.id)}
                      >
                        مشاهده جزئیات{' '}
                        <span aria-hidden="true">←</span>
                      </button>
                    </div>
                  </article>
                ))}
              </div>
            )}
          </section>
        )}

        {!selectedEvent && (
          <section className="about-section" id="about">
            <span className="eyebrow">EVENT PLANET</span>
            <h2>هر رویداد، شروع یک فرصت تازه است.</h2>
            <p>
              یک مکان برای کشف تجربه‌ها، یادگیری و ارتباط با دیگران.
            </p>
          </section>
        )}
      </main>

      <footer className="footer">
        <a className="brand" href="#home">
          <span className="brand-icon">E</span>
          <span>
            EVENT <strong>PLANET</strong>
          </span>
        </a>

        <span>ساخته‌شده برای تجربه‌های بهتر ✦</span>
      </footer>
    </div>
  )
}

export default App

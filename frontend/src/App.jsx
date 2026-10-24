
import { useEffect, useState } from 'react'
import { apiRequest } from './api/client'

const emptyVehicle = {
  make: '',
  model: '',
  category: '',
  price: '',
  quantity: 0,
}

function App() {
  const [vehicles, setVehicles] = useState([])
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('All')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [purchasingId, setPurchasingId] = useState(null)

  const [token, setToken] = useState(
    () => localStorage.getItem('accessToken') || '',
  )
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [email, setEmail] = useState('')
  const [mode, setMode] = useState('login')
  const [authLoading, setAuthLoading] = useState(false)

  const [isAdmin, setIsAdmin] = useState(
    () => localStorage.getItem('isStaff') === 'true',
  )
  const [vehicleForm, setVehicleForm] = useState(emptyVehicle)
  const [editingId, setEditingId] = useState(null)
  const [savingVehicle, setSavingVehicle] = useState(false)

  async function loadVehicles(accessToken = token) {
    if (!accessToken) {
      setVehicles([])
      return
    }

    setLoading(true)
    setError('')

    try {
      const data = await apiRequest('/vehicles/', {
        token: accessToken,
      })
      setVehicles(Array.isArray(data) ? data : data.results || [])
    } catch (err) {
      setError(err.message || 'Unable to load vehicles.')
      setVehicles([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadVehicles(token)
  }, [token])

  async function handleAuth(event) {
    event.preventDefault()
    setAuthLoading(true)
    setError('')
    setMessage('')

    try {
      if (mode === 'register') {
        await apiRequest('/auth/register/', {
          method: 'POST',
          body: JSON.stringify({ username, email, password }),
        })

        setMessage('Registration successful. You can now log in.')
        setMode('login')
        setPassword('')
      } else {
        const result = await apiRequest('/auth/login/', {
          method: 'POST',
          body: JSON.stringify({ username, password }),
        })

        localStorage.setItem('accessToken', result.access)
        localStorage.setItem('refreshToken', result.refresh)
        localStorage.setItem('isStaff', String(result.is_staff))

        setToken(result.access)
        setIsAdmin(result.is_staff === true)
        setPassword('')
        setMessage(`Welcome, ${result.username || username}!`)
      }
    } catch (err) {
      setError(err.message || 'Authentication failed.')
    } finally {
      setAuthLoading(false)
    }
  }

  function logout() {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('isStaff')

    setToken('')
    setIsAdmin(false)
    setVehicles([])
    setVehicleForm(emptyVehicle)
    setEditingId(null)
    setMessage('You have logged out.')
    setError('')
  }

  async function purchaseVehicle(id) {
    if (!token) {
      setError('Please log in before purchasing a vehicle.')
      return
    }

    setPurchasingId(id)
    setError('')
    setMessage('')

    try {
      await apiRequest(`/vehicles/${id}/purchase/`, {
        method: 'POST',
        token,
      })

      setMessage('Purchase successful.')
      await loadVehicles(token)
    } catch (err) {
      setError(err.message || 'Purchase failed.')
    } finally {
      setPurchasingId(null)
    }
  }

  function handleVehicleInput(event) {
    const { name, value } = event.target
    setVehicleForm((previous) => ({ ...previous, [name]: value }))
  }

  async function handleVehicleSubmit(event) {
    event.preventDefault()

    if (!isAdmin) {
      setError('Only administrators can manage vehicles.')
      return
    }

    setSavingVehicle(true)
    setError('')
    setMessage('')

    try {
      const payload = {
        ...vehicleForm,
        price: Number(vehicleForm.price),
        quantity: Number(vehicleForm.quantity),
      }

      if (editingId !== null) {
        await apiRequest(`/vehicles/${editingId}/`, {
          method: 'PUT',
          token,
          body: JSON.stringify(payload),
        })
        setMessage('Vehicle updated successfully.')
      } else {
        await apiRequest('/vehicles/', {
          method: 'POST',
          token,
          body: JSON.stringify(payload),
        })
        setMessage('Vehicle added successfully.')
      }

      setVehicleForm(emptyVehicle)
      setEditingId(null)
      await loadVehicles(token)
    } catch (err) {
      setError(err.message || 'Unable to save vehicle.')
    } finally {
      setSavingVehicle(false)
    }
  }

  function startEditing(vehicle) {
    setEditingId(vehicle.id)
    setVehicleForm({
      make: vehicle.make,
      model: vehicle.model,
      category: vehicle.category,
      price: String(vehicle.price),
      quantity: vehicle.quantity,
    })
    setError('')
    setMessage('')
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  function cancelEditing() {
    setEditingId(null)
    setVehicleForm(emptyVehicle)
    setError('')
  }

  async function deleteVehicle(vehicle) {
    if (!isAdmin) return

    const confirmed = window.confirm(
      `Are you sure you want to delete ${vehicle.make} ${vehicle.model}?`,
    )
    if (!confirmed) return

    setError('')
    setMessage('')

    try {
      await apiRequest(`/vehicles/${vehicle.id}/`, {
        method: 'DELETE',
        token,
      })

      setMessage('Vehicle deleted successfully.')
      await loadVehicles(token)
    } catch (err) {
      setError(err.message || 'Unable to delete vehicle.')
    }
  }

  async function restockVehicle(vehicle) {
    if (!isAdmin) return

    const input = window.prompt(
      `How many units of ${vehicle.make} ${vehicle.model} should be added?`,
      '1',
    )

    if (input === null) return

    const quantity = Number(input)

    if (!Number.isInteger(quantity) || quantity <= 0) {
      setError('Enter a positive whole number for the restock quantity.')
      return
    }

    setError('')
    setMessage('')

    try {
      await apiRequest(`/vehicles/${vehicle.id}/restock/`, {
        method: 'POST',
        token,
        body: JSON.stringify({ quantity }),
      })

      setMessage('Vehicle restocked successfully.')
      await loadVehicles(token)
    } catch (err) {
      setError(err.message || 'Unable to restock vehicle.')
    }
  }

  const filteredVehicles = vehicles.filter((vehicle) => {
    const text =
      `${vehicle.make} ${vehicle.model} ${vehicle.category}`.toLowerCase()

    return (
      text.includes(search.toLowerCase()) &&
      (category === 'All' || vehicle.category === category)
    )
  })

  const categories = [
    'All',
    ...new Set(vehicles.map((vehicle) => vehicle.category)),
  ]

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <header className="bg-slate-950 text-white">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-6 py-5">
          <div>
            <h1 className="text-2xl font-bold">Incubyte Motors</h1>
            <p className="text-sm text-slate-400">Find your next drive</p>
          </div>

          {token ? (
            <div className="flex items-center gap-3">
              <span className="text-sm text-slate-300">
                {isAdmin ? 'Admin' : 'Signed in'}
              </span>
              <button
                onClick={logout}
                className="rounded-lg border border-slate-600 px-4 py-2 hover:bg-slate-800"
              >
                Logout
              </button>
            </div>
          ) : (
            <button
              onClick={() => {
                setMode(mode === 'login' ? 'register' : 'login')
                setError('')
                setMessage('')
              }}
              className="rounded-lg bg-blue-600 px-4 py-2 font-semibold hover:bg-blue-500"
            >
              {mode === 'login' ? 'Register' : 'Back to Login'}
            </button>
          )}
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-6 py-10">
        {!token && (
          <section className="mx-auto mb-10 max-w-lg rounded-2xl bg-white p-8 shadow-sm">
            <h2 className="mb-2 text-2xl font-bold">
              {mode === 'login' ? 'Welcome back' : 'Create your account'}
            </h2>
            <p className="mb-6 text-slate-500">
              {mode === 'login'
                ? 'Log in to access the dealership inventory.'
                : 'Register to start exploring our vehicles.'}
            </p>

            <form onSubmit={handleAuth} className="space-y-4">
              <label className="block">
                <span className="mb-1 block text-sm font-medium">Username</span>
                <input
                  required
                  autoComplete="username"
                  value={username}
                  onChange={(event) => setUsername(event.target.value)}
                  className="w-full rounded-lg border border-slate-300 px-4 py-3"
                />
              </label>

              {mode === 'register' && (
                <label className="block">
                  <span className="mb-1 block text-sm font-medium">Email</span>
                  <input
                    required
                    type="email"
                    autoComplete="email"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    className="w-full rounded-lg border border-slate-300 px-4 py-3"
                  />
                </label>
              )}

              <label className="block">
                <span className="mb-1 block text-sm font-medium">Password</span>
                <input
                  required
                  minLength={8}
                  type="password"
                  autoComplete={
                    mode === 'login' ? 'current-password' : 'new-password'
                  }
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  className="w-full rounded-lg border border-slate-300 px-4 py-3"
                />
              </label>

              <button
                disabled={authLoading}
                className="w-full rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-500 disabled:opacity-60"
              >
                {authLoading
                  ? 'Please wait...'
                  : mode === 'login'
                    ? 'Login'
                    : 'Create Account'}
              </button>
            </form>

            <p className="mt-4 text-center text-sm text-slate-500">
              {mode === 'login'
                ? 'New to Incubyte Motors?'
                : 'Already have an account?'}{' '}
              <button
                onClick={() => {
                  setMode(mode === 'login' ? 'register' : 'login')
                  setError('')
                  setMessage('')
                }}
                className="font-semibold text-blue-600 hover:underline"
              >
                {mode === 'login' ? 'Register' : 'Login'}
              </button>
            </p>
          </section>
        )}

        <section className="mb-10 rounded-2xl bg-gradient-to-r from-blue-950 to-slate-800 p-8 text-white md:p-12">
          <p className="mb-3 font-semibold uppercase tracking-widest text-blue-300">
            Explore our collection
          </p>
          <h2 className="mb-4 text-3xl font-bold md:text-5xl">
            The right car for your next journey.
          </h2>
          <p className="max-w-2xl text-slate-300">
            Browse the inventory and find a vehicle that suits your needs.
          </p>
        </section>

        {error && (
          <div role="alert" className="mb-5 rounded-lg bg-red-50 p-4 text-red-700">
            {error}
          </div>
        )}

        {message && (
          <div role="status" className="mb-5 rounded-lg bg-green-50 p-4 text-green-800">
            {message}
          </div>
        )}

        {token && isAdmin && (
          <section className="mb-10 rounded-2xl bg-white p-6 shadow-sm md:p-8">
            <h2 className="mb-2 text-2xl font-bold">
              {editingId !== null ? 'Edit Vehicle' : 'Add New Vehicle'}
            </h2>
            <p className="mb-6 text-sm text-slate-500">
              Admin inventory management
            </p>

            <form onSubmit={handleVehicleSubmit} className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
              <input
                required
                name="make"
                value={vehicleForm.make}
                onChange={handleVehicleInput}
                placeholder="Make (e.g. Toyota)"
                className="rounded-lg border border-slate-300 px-4 py-3"
              />
              <input
                required
                name="model"
                value={vehicleForm.model}
                onChange={handleVehicleInput}
                placeholder="Model (e.g. Camry)"
                className="rounded-lg border border-slate-300 px-4 py-3"
              />
              <input
                required
                name="category"
                value={vehicleForm.category}
                onChange={handleVehicleInput}
                placeholder="Category (e.g. Sedan)"
                className="rounded-lg border border-slate-300 px-4 py-3"
              />
              <input
                required
                min="0.01"
                step="0.01"
                type="number"
                name="price"
                value={vehicleForm.price}
                onChange={handleVehicleInput}
                placeholder="Price"
                className="rounded-lg border border-slate-300 px-4 py-3"
              />
              <input
                required
                min="0"
                step="1"
                type="number"
                name="quantity"
                value={vehicleForm.quantity}
                onChange={handleVehicleInput}
                placeholder="Quantity"
                className="rounded-lg border border-slate-300 px-4 py-3"
              />

              <div className="flex flex-wrap gap-3 sm:col-span-2 lg:col-span-5">
                <button
                  type="submit"
                  disabled={savingVehicle}
                  className="rounded-lg bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-500 disabled:opacity-60"
                >
                  {savingVehicle
                    ? 'Saving...'
                    : editingId !== null
                      ? 'Save Changes'
                      : 'Add Vehicle'}
                </button>

                {editingId !== null && (
                  <button
                    type="button"
                    onClick={cancelEditing}
                    className="rounded-lg border border-slate-300 px-5 py-3 hover:bg-slate-50"
                  >
                    Cancel
                  </button>
                )}
              </div>
            </form>
          </section>
        )}

        <section>
          <div className="mb-6 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div>
              <h2 className="text-2xl font-bold">Available vehicles</h2>
              <p className="mt-1 text-slate-500">
                {filteredVehicles.length} vehicles found
              </p>
            </div>

            <div className="flex flex-col gap-3 sm:flex-row">
              <input
                type="search"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Search vehicles..."
                className="rounded-lg border border-slate-300 bg-white px-4 py-3"
              />

              <select
                value={category}
                onChange={(event) => setCategory(event.target.value)}
                className="rounded-lg border border-slate-300 bg-white px-4 py-3"
              >
                {categories.map((item) => (
                  <option key={item} value={item}>
                    {item === 'All' ? 'All categories' : item}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {loading ? (
            <p className="py-12 text-center text-slate-500">
              Loading vehicles...
            </p>
          ) : filteredVehicles.length === 0 ? (
            <p className="rounded-xl bg-white py-12 text-center text-slate-500">
              No vehicles found. Log in to view your inventory, or add vehicles
              to the database.
            </p>
          ) : (
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {filteredVehicles.map((vehicle) => (
                <article
                  key={vehicle.id}
                  className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
                >
                  <div className="h-44 overflow-hidden bg-slate-100">
                    <img
                      src={
                        vehicle.model.toLowerCase().includes('civic')
                          ? '/cars/honda-civic.jpg'
                          : vehicle.model.toLowerCase().includes('innova')
                            ? '/cars/toyota-innova.jpg'
                            : vehicle.model.toLowerCase().includes('camry')
                              ? '/cars/toyota-camry.jpg'
                              : vehicle.model.toLowerCase().includes('creta')
                                ? '/cars/hyundai-creta.jpg'
                                : vehicle.model.toLowerCase().includes('swift')
                                  ? '/cars/maruti-swift.jpg'
                                  : vehicle.model.toLowerCase().includes('3 series')
                                    ? '/cars/bmw-3-series.jpg'
                                    : vehicle.model.toLowerCase().includes('nexon')
                                      ? '/cars/tata-nexon.jpg'
                                      : '/cars/toyota-camry.jpg'
                      }
                      alt={`${vehicle.make} ${vehicle.model}`}
                      className="h-full w-full object-cover transition-transform duration-300 hover:scale-105"
                      onError={(event) => {
                        event.currentTarget.style.display = 'none'
                      }}
                    />
                  </div>

                  <div className="p-6">
                    <p className="text-sm font-medium text-blue-600">
                      {vehicle.category}
                    </p>
                    <h3 className="mt-1 text-xl font-bold">
                      {vehicle.make} {vehicle.model}
                    </h3>
                    <p className="mt-3 text-2xl font-bold">
                      ${Number(vehicle.price).toLocaleString('en-US')}
                    </p>
                    <p className="mt-2 text-sm text-slate-500">
                      {vehicle.quantity > 0
                        ? `${vehicle.quantity} in stock`
                        : 'Out of stock'}
                    </p>

                    <button
                      onClick={() => purchaseVehicle(vehicle.id)}
                      disabled={
                        !token ||
                        vehicle.quantity === 0 ||
                        purchasingId === vehicle.id
                      }
                      className="mt-5 w-full rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-500 disabled:cursor-not-allowed disabled:bg-slate-300 disabled:text-slate-500"
                    >
                      {!token
                        ? 'Login to Purchase'
                        : purchasingId === vehicle.id
                          ? 'Processing...'
                          : vehicle.quantity > 0
                            ? 'Purchase'
                            : 'Unavailable'}
                    </button>

                    {token && isAdmin && (
                      <div className="mt-3 grid grid-cols-3 gap-2">
                        <button
                          onClick={() => startEditing(vehicle)}
                          className="rounded-lg bg-amber-100 px-2 py-2 text-sm font-semibold text-amber-900 hover:bg-amber-200"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => restockVehicle(vehicle)}
                          className="rounded-lg bg-green-100 px-2 py-2 text-sm font-semibold text-green-900 hover:bg-green-200"
                        >
                          Restock
                        </button>
                        <button
                          onClick={() => deleteVehicle(vehicle)}
                          className="rounded-lg bg-red-100 px-2 py-2 text-sm font-semibold text-red-900 hover:bg-red-200"
                        >
                          Delete
                        </button>
                      </div>
                    )}
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </main>

      <footer className="mt-12 bg-slate-950 px-6 py-6 text-center text-sm text-slate-400">
        Incubyte Motors · Car Dealership Inventory System
      </footer>
    </div>
  )
}

export default App

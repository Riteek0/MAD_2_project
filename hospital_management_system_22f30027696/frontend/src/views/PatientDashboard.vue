<template>
  <div>

    <!-- Navbar -->
    <nav class="navbar px-4 py-3" style="background:#1e1e2f;">
      <span class="fw-bold fs-5" style="color:#a78bfa;">MediCare HMS</span>
      <div class="d-flex gap-2">
        <button class="btn btn-sm" style="background:#7c3aed;color:#fff;border:none;" @click="openEditProfile">
          Edit Profile
        </button>
        <button class="btn btn-sm" style="background:#ef4444;color:#fff;border:none;" @click="logout">
          Logout
        </button>
      </div>
    </nav>

    <div class="container mt-4">

      <!-- Welcome -->
      <h5 class="mb-4" style="color:#1e1e2f;">Welcome, {{ name }}</h5>

      <!-- Search Doctors -->
      <div class="card mb-4 border-0 shadow-sm">
        <div class="card-header border-0 fw-semibold" style="background:#f0f4ff;color:#3730a3;">
          Search Doctors
        </div>
        <div class="card-body">
          <div class="row g-2 align-items-center">
            <div class="col-md-5">
              <input
                v-model="doctorNameSearch"
                class="form-control"
                placeholder="Search by doctor name..."
                @keyup.enter="searchDoctorsByName"
                style="border-color:#c7d2fe;"
              />
            </div>
            <div class="col-auto">
              <button
                class="btn btn-sm fw-semibold"
                style="background:#0891b2;color:#fff;border:none;"
                @click="searchDoctorsByName"
              >Search</button>
            </div>
            <div class="col-auto">
              <button
                class="btn btn-sm fw-semibold"
                style="background:#64748b;color:#fff;border:none;"
                @click="clearSearch"
              >Clear</button>
            </div>
          </div>

          <!-- Search Results -->
          <div v-if="searchedDoctors.length" class="mt-3">
            <p class="text-muted small mb-2">{{ searchedDoctors.length }} result(s) found</p>
            <div class="row g-2">
              <div class="col-md-6" v-for="d in searchedDoctors" :key="d.id">
                <div class="card border-0 shadow-sm">
                  <div class="card-body py-2">
                    <p class="fw-semibold mb-1">{{ d.name }}</p>
                    <p class="text-muted small mb-2">{{ d.specialization }} — {{ d.department }}</p>
                    <div class="d-flex gap-2">
                      <button
                        class="btn btn-sm"
                        style="background:#e0e7ff;color:#4f46e5;border:none;"
                        @click="viewProfile(d.id)"
                      >View Profile</button>
                      <router-link
                        :to="`/book?doctor_id=${d.id}&doctor_name=${d.name}`"
                        class="btn btn-sm"
                        style="background:#059669;color:#fff;border:none;"
                      >Book</router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <p v-if="noSearchResults" class="text-danger small mt-2">No doctors found.</p>
        </div>
      </div>

      <!-- Select Department -->
      <div class="card mb-4 border-0 shadow-sm">
        <div class="card-header border-0 fw-semibold" style="background:#f0f4ff;color:#3730a3;">
          Select Department
        </div>
        <div class="card-body">
          <div class="row g-2">
            <div class="col-md-3 col-6" v-for="d in departments" :key="d.id">
              <div
                class="card text-center py-2 px-1 border-0"
                :style="selectedDept === d.id
                  ? 'background:#4f46e5;color:#fff;cursor:pointer;'
                  : 'background:#f8fafc;color:#1e1e2f;cursor:pointer;border:1px solid #e2e8f0;'"
                @click="selectDept(d.id)"
              >
                <p class="fw-semibold mb-0 small">{{ d.name }}</p>
                <p class="mb-0 small"
                  :style="selectedDept === d.id ? 'color:#c7d2fe;' : 'color:#94a3b8;'">
                  {{ d.description }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Available Doctors -->
      <div v-if="doctors.length" class="card mb-4 border-0 shadow-sm">
        <div class="card-header border-0 fw-semibold" style="background:#f0f4ff;color:#3730a3;">
          Available Doctors
        </div>
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-6" v-for="d in doctors" :key="d.id">
              <div class="card border-0 shadow-sm h-100" style="border-left:4px solid #4f46e5 !important;">
                <div class="card-body">
                  <p class="fw-semibold mb-1">{{ d.name }}</p>
                  <span class="badge mb-1" style="background:#dbeafe;color:#1d4ed8;">
                    {{ d.specialization }}
                  </span>
                  <p class="text-muted small mb-2">{{ d.department }}</p>
                  <div class="d-flex gap-2">
                    <button
                      class="btn btn-sm"
                      style="background:#e0e7ff;color:#4f46e5;border:none;"
                      @click="viewProfile(d.id)"
                    >View Profile & Availability</button>
                    <router-link
                      :to="`/book?doctor_id=${d.id}&doctor_name=${d.name}`"
                      class="btn btn-sm"
                      style="background:#059669;color:#fff;border:none;"
                    >Book</router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Upcoming Appointments -->
      <div class="card mb-4 border-0 shadow-sm">
        <div class="card-header border-0 fw-semibold" style="background:#fff7ed;color:#c2410c;">
          Upcoming Appointments
        </div>
        <div class="card-body p-0">
          <table class="table table-hover mb-0">
            <thead style="background:#fff7ed;">
              <tr>
                <th>#</th>
                <th>Doctor</th>
                <th>Date</th>
                <th>Time</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="a in upcomingAppointments" :key="a.id">
                <td>{{ a.id }}</td>
                <td>{{ a.doctor_name }}</td>
                <td>{{ a.date }}</td>
                <td>{{ a.time }}</td>
                <td>
                  <span class="badge" style="background:#fef3c7;color:#92400e;">
                    {{ a.status }}
                  </span>
                </td>
                <td>
                  <button
                    class="btn btn-sm"
                    style="background:#fef2f2;color:#dc2626;border:1px solid #fca5a5;"
                    @click="cancelAppointment(a.id)"
                  >Cancel</button>
                </td>
              </tr>
              <tr v-if="!upcomingAppointments.length">
                <td colspan="6" class="text-center text-muted py-3">
                  No upcoming appointments
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Treatment History -->
      <div class="card mb-4 border-0 shadow-sm">
        <div class="card-header border-0 d-flex justify-content-between align-items-center"
          style="background:#f0fdf4;color:#166534;">
          <span class="fw-semibold">Treatment History</span>
          <button
            class="btn btn-sm"
            style="background:#059669;color:#fff;border:none;"
            @click="exportCSV"
          >Export CSV</button>
        </div>
        <p v-if="exportMsg" class="text-success small px-3 pt-2">{{ exportMsg }}</p>
        <div class="card-body p-0">
          <table class="table table-hover mb-0">
            <thead style="background:#f0fdf4;">
              <tr>
                <th>Doctor</th>
                <th>Date</th>
                <th>Status</th>
                <th>Diagnosis</th>
                <th>Prescription</th>
                <th>Next Visit</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="a in pastAppointments" :key="a.id">
                <td>{{ a.doctor_name }}</td>
                <td>{{ a.date }}</td>
                <td>
                  <span
                    class="badge"
                    :style="a.status === 'completed'
                      ? 'background:#dcfce7;color:#166534;'
                      : 'background:#fee2e2;color:#991b1b;'"
                  >{{ a.status }}</span>
                </td>
                <td>{{ a.diagnosis    || '—' }}</td>
                <td>{{ a.prescription || '—' }}</td>
                <td>{{ a.next_visit_date || '—' }}</td>
              </tr>
              <tr v-if="!pastAppointments.length">
                <td colspan="6" class="text-center text-muted py-3">
                  No history found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- Doctor Profile Modal -->
    <div v-if="profileModal" class="modal d-block" style="background:rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-lg">
        <div class="modal-content border-0 shadow">
          <div class="modal-header" style="background:#1e1e2f;">
            <h6 class="modal-title" style="color:#a78bfa;">Doctor Profile</h6>
            <button class="btn-close btn-close-white" @click="profileModal = false"></button>
          </div>
          <div class="modal-body">
            <table class="table table-sm table-borderless">
              <tbody>
                <tr>
                  <td class="text-muted" style="width:140px">Name</td>
                  <td><strong>{{ selectedDoctor.name }}</strong></td>
                </tr>
                <tr>
                  <td class="text-muted">Specialization</td>
                  <td>{{ selectedDoctor.specialization }}</td>
                </tr>
                <tr>
                  <td class="text-muted">Department</td>
                  <td>{{ selectedDoctor.department }}</td>
                </tr>
                <tr>
                  <td class="text-muted">Email</td>
                  <td>{{ selectedDoctor.email }}</td>
                </tr>
              </tbody>
            </table>
            <hr/>
            <p class="fw-semibold mb-2">Availability — Next 7 Days</p>
            <div v-if="selectedDoctor.availability && selectedDoctor.availability.length">
              <div class="row g-2">
                <div class="col-md-6" v-for="(slot, i) in selectedDoctor.availability" :key="i">
                  <div class="card border-0" style="background:#f0fdf4;border-left:3px solid #059669 !important;">
                    <div class="card-body py-2">
                      <p class="fw-semibold mb-1" style="color:#059669;">{{ slot.date }}</p>
                      <p class="mb-0 small text-muted">{{ slot.start }} to {{ slot.end }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="alert" style="background:#fef3c7;color:#92400e;border:none;">
              No availability set for this doctor.
            </div>
          </div>
          <div class="modal-footer">
            <router-link
              :to="`/book?doctor_id=${selectedDoctor.id}&doctor_name=${selectedDoctor.name}`"
              class="btn"
              style="background:#059669;color:#fff;border:none;"
              @click="profileModal = false"
            >Book Appointment</router-link>
            <button
              class="btn"
              style="background:#64748b;color:#fff;border:none;"
              @click="profileModal = false"
            >Close</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Profile Modal -->
    <div v-if="editModal" class="modal d-block" style="background:rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content border-0 shadow">
          <div class="modal-header" style="background:#1e1e2f;">
            <h6 class="modal-title" style="color:#a78bfa;">Edit Profile</h6>
            <button class="btn-close btn-close-white" @click="editModal = false"></button>
          </div>
          <div class="modal-body">
            <div class="mb-2">
              <label class="form-label">Full Name</label>
              <input v-model="profile.name" class="form-control" style="border-color:#c7d2fe;" />
            </div>
            <div class="mb-2">
              <label class="form-label">Age</label>
              <input v-model="profile.age" class="form-control" style="border-color:#c7d2fe;" />
            </div>
            <div class="mb-2">
              <label class="form-label">Phone</label>
              <input v-model="profile.phone" class="form-control" style="border-color:#c7d2fe;" />
            </div>
            <div class="mb-2">
              <label class="form-label">Address</label>
              <textarea v-model="profile.address" class="form-control" rows="2"
                style="border-color:#c7d2fe;"></textarea>
            </div>
            <div class="mb-2">
              <label class="form-label">Gender</label>
              <select v-model="profile.gender" class="form-select" style="border-color:#c7d2fe;">
                <option value="">Select</option>
                <option>Male</option>
                <option>Female</option>
                <option>Other</option>
              </select>
            </div>
            <p v-if="profileMsg" class="text-success small">{{ profileMsg }}</p>
          </div>
          <div class="modal-footer">
            <button
              class="btn"
              style="background:#7c3aed;color:#fff;border:none;"
              @click="saveProfile"
            >Save</button>
            <button
              class="btn"
              style="background:#64748b;color:#fff;border:none;"
              @click="editModal = false"
            >Cancel</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      name: localStorage.getItem('name'),
      departments: [],
      doctors: [],
      history: [],
      selectedDept: null,

      doctorNameSearch: '',
      searchedDoctors: [],
      noSearchResults: false,

      profileModal: false,
      selectedDoctor: {},

      editModal: false,
      profile: { name: '', age: '', phone: '', address: '', gender: '' },
      profileMsg: '',

      exportMsg: ''
    }
  },

  computed: {
    upcomingAppointments() {
      return this.history.filter(a => a.status === 'pending')
    },
    pastAppointments() {
      return this.history.filter(a => a.status !== 'pending')
    }
  },

  async mounted() {
    await this.load()
  },

  methods: {
    headers() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}` }
    },

    async load() {
      try {
        const [deptsRes, histRes] = await Promise.all([
          axios.get('http://127.0.0.1:5000/api/patient/departments',
            { headers: this.headers() }),
          axios.get('http://127.0.0.1:5000/api/patient/history',
            { headers: this.headers() })
        ])
        this.departments = deptsRes.data
        this.history     = histRes.data
      } catch (e) {
        if (e.response?.status === 401) {
          localStorage.clear()
          this.$router.push('/login')
        }
      }
    },

    async selectDept(id) {
      this.selectedDept = id
      const res = await axios.get(
        `http://127.0.0.1:5000/api/patient/doctors?department_id=${id}`,
        { headers: this.headers() }
      )
      this.doctors = res.data
    },

    async searchDoctorsByName() {
      this.noSearchResults = false
      this.searchedDoctors = []
      if (!this.doctorNameSearch.trim()) return
      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/api/patient/search-doctors?name=${this.doctorNameSearch}`,
          { headers: this.headers() }
        )
        this.searchedDoctors = res.data
        if (!this.searchedDoctors.length) this.noSearchResults = true
      } catch (e) { this.noSearchResults = true }
    },

    clearSearch() {
      this.doctorNameSearch = ''
      this.searchedDoctors  = []
      this.noSearchResults  = false
    },

    async viewProfile(doctor_id) {
      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/api/patient/doctor-profile/${doctor_id}`,
          { headers: this.headers() }
        )
        this.selectedDoctor = res.data
        this.profileModal   = true
      } catch (e) { alert('Could not load doctor profile.') }
    },

    async cancelAppointment(id) {
      if (!confirm('Cancel this appointment?')) return
      try {
        await axios.put(
          `http://127.0.0.1:5000/api/patient/cancel/${id}`,
          {}, { headers: this.headers() }
        )
        await this.load()
      } catch (e) { alert('Failed to cancel.') }
    },

    openEditProfile() {
      this.profile    = { name: localStorage.getItem('name') || '',
                          age: '', phone: '', address: '', gender: '' }
      this.profileMsg = ''
      this.editModal  = true
    },

    async saveProfile() {
      try {
        await axios.put(
          'http://127.0.0.1:5000/api/patient/profile',
          this.profile, { headers: this.headers() }
        )
        this.profileMsg = 'Profile updated successfully'
        localStorage.setItem('name', this.profile.name)
        this.name = this.profile.name
        setTimeout(() => { this.editModal = false; this.profileMsg = '' }, 1200)
      } catch (e) { alert('Failed to update profile.') }
    },

    async exportCSV() {
      try {
        await axios.post(
          'http://127.0.0.1:5000/api/patient/export-csv',
          {}, { headers: this.headers() }
        )
        this.exportMsg = 'Export started. You will receive an email shortly.'
        setTimeout(() => this.exportMsg = '', 5000)
      } catch (e) { alert('Export failed.') }
    },

    logout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  }
}
</script>
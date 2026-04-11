<template>
  <div class="container-fluid mt-4">

    <div class="d-flex justify-content-between align-items-center mb-4">
      <h4 class="fw-bold" style="color:#3730a3;">Admin Dashboard</h4>
      <button class="btn btn-sm btn-outline-danger" @click="logout">Logout</button>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-md-4">
        <div class="card border-0 shadow-sm text-center p-3" style="background:#f0f4ff;">
          <div class="fs-2 fw-bold" style="color:#3730a3;">{{ stats.total_doctors }}</div>
          <div class="text-muted small">Total Doctors</div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm text-center p-3" style="background:#f0fdf4;">
          <div class="fs-2 fw-bold" style="color:#166534;">{{ stats.total_patients }}</div>
          <div class="text-muted small">Total Patients</div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm text-center p-3" style="background:#fff7ed;">
          <div class="fs-2 fw-bold" style="color:#9a3412;">{{ stats.total_appointments }}</div>
          <div class="text-muted small">Total Appointments</div>
        </div>
      </div>
    </div>

    <ul class="nav nav-tabs mb-3">
      <li class="nav-item">
        <a class="nav-link" :class="{ active: tab === 'doctors' }" href="#" @click.prevent="tab = 'doctors'">Doctors</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: tab === 'patients' }" href="#" @click.prevent="tab = 'patients'">Patients</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: tab === 'appointments' }" href="#" @click.prevent="tab = 'appointments'">Appointments</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: tab === 'add' }" href="#" @click.prevent="tab = 'add'">Add Doctor</a>
      </li>
    </ul>

    <!-- DOCTORS TAB -->
    <div v-if="tab === 'doctors'">
      <div class="mb-3 d-flex gap-2">
        <input v-model="searchDoctor" class="form-control w-25" placeholder="Search by name " />
        <button class="btn btn-sm" style="background:#4f46e5;color:#fff;" @click="searchDoctors">Search</button>
        <button class="btn btn-sm btn-outline-secondary" @click="loadDoctors">Reset</button>
      </div>
      <div class="table-responsive">
        <table class="table table-bordered table-hover align-middle">
          <thead style="background:#f0f4ff;">
            <tr>
              <th>#</th>
              <th>Name</th>
              <th>Email</th>
              <th>Specialization</th>
              <th>Department</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="d in doctors" :key="d.doctor_id">
              <td>{{ d.doctor_id }}</td>
              <td>{{ d.name }}</td>
              <td>{{ d.email }}</td>
              <td>{{ d.specialization }}</td>
              <td>{{ d.department }}</td>
              <td>
                <span class="badge"
                  :style="d.is_blacklisted
                    ? 'background:#fee2e2;color:#991b1b;'
                    : 'background:#dcfce7;color:#166534;'">
                  {{ d.is_blacklisted ? 'Blacklisted' : 'Active' }}
                </span>
              </td>
              <td class="d-flex gap-1 flex-wrap">
                <button class="btn btn-sm"
                  style="background:#e0e7ff;color:#3730a3;"
                  @click="openEditDoctor(d)">Edit</button>
                <button class="btn btn-sm"
                  style="background:#fee2e2;color:#dc2626;"
                  @click="removeDoctor(d.doctor_id)">Remove</button>
                <button v-if="!d.is_blacklisted"
                  class="btn btn-sm"
                  style="background:#fef2f2;color:#dc2626;border:1px solid #fca5a5;"
                  @click="blacklistDoctor(d.id)">Blacklist</button>
                <button v-else
                  class="btn btn-sm"
                  style="background:#f0fdf4;color:#16a34a;border:1px solid #86efac;"
                  @click="whitelistDoctor(d.id)">Whitelist</button>
              </td>
            </tr>
            <tr v-if="doctors.length === 0">
              <td colspan="7" class="text-center text-muted">No doctors found</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- PATIENTS TAB -->
    <div v-if="tab === 'patients'">
      <div class="mb-3 d-flex gap-2">
        <input v-model="searchPatient" class="form-control w-25" placeholder="Search by name " />
        <button class="btn btn-sm" style="background:#4f46e5;color:#fff;" @click="searchPatients">Search</button>
        <button class="btn btn-sm btn-outline-secondary" @click="loadPatients">Reset</button>
      </div>
      <div class="table-responsive">
        <table class="table table-bordered table-hover align-middle">
          <thead style="background:#f0f4ff;">
            <tr>
              <th>#</th>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Age</th>
              <th>Address</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in patients" :key="p.id">
              <td>{{ p.id }}</td>
              <td>{{ p.name }}</td>
              <td>{{ p.email }}</td>
              <td>{{ p.phone }}</td>
              <td>{{ p.age }}</td>
              <td>{{ p.address }}</td>
              <td>
                <span class="badge"
                  :style="p.is_blacklisted
                    ? 'background:#fee2e2;color:#991b1b;'
                    : 'background:#dcfce7;color:#166534;'">
                  {{ p.is_blacklisted ? 'Blacklisted' : 'Active' }}
                </span>
              </td>

            </tr>
            <tr v-if="patients.length === 0">
              <td colspan="7" class="text-center text-muted">No patients found</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- APPOINTMENTS TAB -->
    <div v-if="tab === 'appointments'">
      <div class="table-responsive">
        <table class="table table-bordered table-hover align-middle">
          <thead style="background:#f0f4ff;">
            <tr>
              <th>#</th>
              <th>Patient</th>
              <th>Doctor</th>
              <th>Date</th>
              <th>Time</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in appointments" :key="a.id">
              <td>{{ a.id }}</td>
              <td>{{ a.patient_name }}</td>
              <td>{{ a.doctor_name }}</td>
              <td>{{ a.date }}</td>
              <td>{{ a.time }}</td>
              <td>
                <span class="badge"
                  :style="a.status === 'completed' ? 'background:#dcfce7;color:#166534;'
                        : a.status === 'cancelled'  ? 'background:#fee2e2;color:#991b1b;'
                        :                             'background:#fef9c3;color:#854d0e;'">
                  {{ a.status }}
                </span>
              </td>
            </tr>
            <tr v-if="appointments.length === 0">
              <td colspan="6" class="text-center text-muted">No appointments found</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ADD DOCTOR TAB -->
    <div v-if="tab === 'add'">
      <div class="card border-0 shadow-sm mx-auto" style="max-width:480px;">
        <div class="card-header border-0 fw-semibold" style="background:#f0f4ff;color:#3730a3;">
          Add New Doctor
        </div>
        <div class="card-body">
          <div class="mb-3">
            <label class="form-label text-muted small">Full Name</label>
            <input v-model="newDoctor.name" class="form-control" placeholder="Full Name" style="border-color:#c7d2fe;" />
          </div>
          <div class="mb-3">
            <label class="form-label text-muted small">Email</label>
            <input v-model="newDoctor.email" type="email" class="form-control" placeholder="doctor@example.com" style="border-color:#c7d2fe;" />
          </div>
          <div class="mb-3">
            <label class="form-label text-muted small">Password</label>
            <input v-model="newDoctor.password" type="password" class="form-control" style="border-color:#c7d2fe;" />
          </div>
          <div class="mb-3">
            <label class="form-label text-muted small">Specialization</label>
            <input v-model="newDoctor.specialization" class="form-control" placeholder="e.g. Cardiologist" style="border-color:#c7d2fe;" />
          </div>
          <div class="mb-3">
            <label class="form-label text-muted small">Department</label>
            <input v-model="newDoctor.department_name" class="form-control" placeholder="e.g. OPD/ER.." style="border-color:#c7d2fe;" />
          </div>
          <p v-if="addErr" class="text-danger small">{{ addErr }}</p>
          <p v-if="addMsg" class="text-success small">{{ addMsg }}</p>
          <button class="btn w-100 fw-semibold"
            style="background:#4f46e5;color:#fff;border:none;"
            @click="addDoctor" :disabled="addLoading">
            {{ addLoading ? 'Adding...' : 'Add Doctor' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Doctor Modal -->
    <div v-if="editModal" class="modal-backdrop-custom">
      <div class="card border-0 shadow-lg p-4" style="width:400px;border-radius:12px;background:#fff;">
        <h6 class="fw-semibold mb-3" style="color:#3730a3;">Edit Doctor</h6>
        <div class="mb-2">
          <label class="form-label text-muted small">Specialization</label>
          <input v-model="editDoctor.specialization" class="form-control" style="border-color:#c7d2fe;" />
        </div>
        <div class="mb-2">
          <label class="form-label text-muted small">Department</label>
          <input v-model="editDoctor.department_name" class="form-control" style="border-color:#c7d2fe;" />
        </div>
        <div class="mb-3 form-check">
          <input v-model="editDoctor.is_active" type="checkbox" class="form-check-input" id="isActive" />
          <label class="form-check-label text-muted small" for="isActive">Is Active</label>
        </div>
        <p v-if="editErr" class="text-danger small">{{ editErr }}</p>
        <p v-if="editMsg" class="text-success small">{{ editMsg }}</p>
        <div class="d-flex gap-2">
          <button class="btn btn-sm w-100 fw-semibold"
            style="background:#4f46e5;color:#fff;"
            @click="submitEditDoctor">Save</button>
          <button class="btn btn-sm w-100 btn-outline-secondary"
            @click="editModal = false">Cancel</button>
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
      tab: 'doctors',
      stats: { total_doctors: 0, total_patients: 0, total_appointments: 0 },
      doctors: [],
      patients: [],
      appointments: [],
      searchDoctor: '',
      searchPatient: '',
      newDoctor: { name: '', email: '', password: '', specialization: '', department_name: '' },
      addLoading: false,
      addErr: '',
      addMsg: '',
      editModal: false,
      editDoctor: { doctor_id: null, specialization: '', department_name: '', is_active: true },
      editErr: '',
      editMsg: ''
    }
  },

  mounted() {
    this.loadStats()
    this.loadDoctors()
  },

  watch: {
    tab(val) {
      if (val === 'doctors')      this.loadDoctors()
      if (val === 'patients')     this.loadPatients()
      if (val === 'appointments') this.loadAppointments()
    }
  },

  methods: {
    headers() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}` }
    },

    async loadStats() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/admin/dashboard', { headers: this.headers() })
        this.stats = res.data
      } catch (e) {
        console.error('Failed to load stats', e)
      }
    },

    async loadDoctors() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/admin/doctors', { headers: this.headers() })
        this.doctors = res.data
      } catch (e) {
        console.error('Failed to load doctors', e)
      }
    },

    async loadPatients() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/admin/patients', { headers: this.headers() })
        this.patients = res.data
      } catch (e) {
        console.error('Failed to load patients', e)
      }
    },

    async loadAppointments() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/admin/appointments', { headers: this.headers() })
        this.appointments = res.data
      } catch (e) {
        console.error('Failed to load appointments', e)
      }
    },

    async searchDoctors() {
      if (!this.searchDoctor) return this.loadDoctors()
      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/api/admin/search?name=${this.searchDoctor}`,
          { headers: this.headers() }
        )
        this.doctors = res.data
      } catch (e) {
        console.error('Search failed', e)
      }
    },

    async searchPatients() {
      if (!this.searchPatient) return this.loadPatients()
      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/api/admin/search-patient?name=${this.searchPatient}`,
          { headers: this.headers() }
        )
        this.patients = res.data
      } catch (e) {
        console.error('Search failed', e)
      }
    },

    async addDoctor() {
      this.addErr = ''
      this.addMsg = ''
      if (!this.newDoctor.name || !this.newDoctor.email || !this.newDoctor.password) {
        this.addErr = 'Name, email and password are required'
        return
      }
      this.addLoading = true
      try {
        const res = await axios.post(
          'http://127.0.0.1:5000/api/admin/add-doctor',
          this.newDoctor,
          { headers: this.headers() }
        )
        this.addMsg = res.data.message
        this.newDoctor = { name: '', email: '', password: '', specialization: '', department_name: '' }
        this.loadStats()
      } catch (e) {
        this.addErr = e.response?.data?.error || 'Failed to add doctor'
      } finally {
        this.addLoading = false
      }
    },

    async removeDoctor(doctorId) {
      if (!confirm('Remove this doctor permanently?')) return
      try {
        await axios.delete(
          `http://127.0.0.1:5000/api/admin/remove-doctor/${doctorId}`,
          { headers: this.headers() }
        )
        await this.loadDoctors()
        await this.loadStats()
      } catch (e) {
        alert('Failed to remove doctor')
      }
    },

    openEditDoctor(d) {
      this.editDoctor = {
        doctor_id: d.doctor_id,
        specialization: d.specialization,
        department_name: d.department,
        is_active: d.is_active
      }
      this.editErr = ''
      this.editMsg = ''
      this.editModal = true
    },

    async submitEditDoctor() {
      this.editErr = ''
      this.editMsg = ''
      try {
        const res = await axios.put(
          `http://127.0.0.1:5000/api/admin/update-doctor/${this.editDoctor.doctor_id}`,
          {
            specialization: this.editDoctor.specialization,
            department_name: this.editDoctor.department_name,
            is_active: this.editDoctor.is_active
          },
          { headers: this.headers() }
        )
        this.editMsg = res.data.message
        await this.loadDoctors()
        setTimeout(() => { this.editModal = false }, 1000)
      } catch (e) {
        this.editErr = e.response?.data?.error || 'Failed to update doctor'
      }
    },

    async blacklistDoctor(userId) {
      if (!confirm('Blacklist this doctor? They will be hidden from patients.')) return
      try {
        await axios.put(
          `http://127.0.0.1:5000/api/admin/blacklist/${userId}`,
          {},
          { headers: this.headers() }
        )
        await this.loadDoctors()
      } catch (e) {
        alert('Failed to blacklist doctor')
      }
    },

    async whitelistDoctor(userId) {
      if (!confirm('Whitelist this doctor? They will be visible to patients again.')) return
      try {
        await axios.put(
          `http://127.0.0.1:5000/api/admin/whitelist/${userId}`,
          {},
          { headers: this.headers() }
        )
        await this.loadDoctors()
      } catch (e) {
        alert('Failed to whitelist doctor')
      }
    },

    logout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.modal-backdrop-custom {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}
</style>

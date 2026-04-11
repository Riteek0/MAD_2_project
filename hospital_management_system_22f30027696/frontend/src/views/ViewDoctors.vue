<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h5> All Doctors</h5>
      <router-link to="/admin" class="btn btn-sm btn-outline-secondary">← Back</router-link>
    </div>
    <table class="table table-bordered table-hover shadow-sm">
      <thead class="table-dark">
        <tr><th>#</th><th>Name</th><th>Email</th><th>Specialization</th><th>Department</th><th>Status</th><th>Actions</th></tr>
      </thead>
      <tbody>
        <tr v-for="d in doctors" :key="d.doctor_id">
          <td>{{ d.doctor_id }}</td>
          <td>{{ d.name }}</td>
          <td>{{ d.email }}</td>
          <td>{{ d.specialization }}</td>
          <td>{{ d.department }}</td>
          <td>
            <span :class="d.is_active ? 'badge bg-success' : 'badge bg-secondary'">
              {{ d.is_active ? 'Active' : 'Inactive' }}
            </span>
          </td>
          <td>
            <button class="btn btn-danger btn-sm me-1" @click="removeDoctor(d.doctor_id)">🗑 Remove</button>
            <button class="btn btn-warning btn-sm" @click="blacklist(d.id)"> Blacklist</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-if="msg" class="text-success">{{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() { return { doctors: [], msg: '' } },
  async mounted() { await this.load() },
  methods: {
    headers() { return { Authorization: `Bearer ${localStorage.getItem('token')}` } },
    async load() {
      const res = await axios.get('http://127.0.0.1:5000/api/admin/doctors', { headers: this.headers() })
      this.doctors = res.data
    },
    async removeDoctor(doctor_id) {
      if (!confirm('Remove this doctor?')) return
      await axios.delete(`http://127.0.0.1:5000/api/admin/remove-doctor/${doctor_id}`, { headers: this.headers() })
      this.msg = 'Doctor removed '
      await this.load()
    },
    async blacklist(user_id) {
      if (!confirm('Blacklist this user?')) return
      await axios.put(`http://127.0.0.1:5000/api/admin/blacklist/${user_id}`, {}, { headers: this.headers() })
      this.msg = 'User blacklisted '
      await this.load()
    }
  }
}
</script>
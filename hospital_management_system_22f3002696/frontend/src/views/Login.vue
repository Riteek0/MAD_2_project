<template>
  <div class="container d-flex justify-content-center align-items-center" style="min-height:100vh">
    <div class="card shadow p-4" style="width:100%;max-width:420px">
      <h4 class="text-center mb-4">Hospital Management</h4>
      <h6 class="text-center text-muted mb-3">Login</h6>
      <div class="mb-3">
        <label class="form-label">Email</label>
        <input v-model="form.email" type="email" class="form-control" placeholder="Enter email" />
      </div>
      <div class="mb-3">
        <label class="form-label">Password</label>
        <input v-model="form.password" type="password" class="form-control" placeholder="Enter password" />
      </div>
      <p v-if="err" class="text-danger small">{{ err }}</p>
      <button class="btn btn-primary w-100" @click="login">Login</button>
      <p class="text-center mt-3 small">
        Don't have an account?
        <router-link to="/register">Register here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return { form: { email: '', password: '' }, err: '' }
  },
  methods: {
    async login() {
      this.err = ''
      if (!this.form.email || !this.form.password) {
        this.err = 'Email and password are required'; return
      }
      try {
        const res = await axios.post('http://127.0.0.1:5000/api/login', this.form)
        localStorage.setItem('token', res.data.token)
        localStorage.setItem('role', res.data.role)
        localStorage.setItem('name', res.data.name)
        if (res.data.role === 'admin')   this.$router.push('/admin')
        else if (res.data.role === 'doctor') this.$router.push('/doctor')
        else this.$router.push('/patient')
      } catch (e) {
        this.err = e.response?.data?.error || 'Login failed'
      }
    }
  }
}
</script>
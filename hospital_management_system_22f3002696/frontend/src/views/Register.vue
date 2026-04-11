<template>
  <div class="container d-flex justify-content-center align-items-center" style="min-height:100vh">
    <div class="card shadow p-4" style="width:100%;max-width:480px">
      <h5 class="text-center mb-4"> Patient Registration</h5>

      <div class="mb-2">
        <label class="form-label">Full Name</label>
        <input v-model="form.name" class="form-control" placeholder="Your full name" />
      </div>

      <div class="mb-2">
        <label class="form-label">Email</label>
        <input v-model="form.email" type="email" class="form-control" placeholder="Email address" />
      </div>

      <div class="mb-2">
        <label class="form-label">Password</label>
        <input v-model="form.password" type="password" class="form-control" placeholder="Password" />
      </div>

      <div class="row">
        <div class="col mb-2">
          <label class="form-label">Age</label>
          <input v-model="form.age" class="form-control" placeholder="Age" />
        </div>
        <div class="col mb-2">
          <label class="form-label">Gender</label>
          <select v-model="form.gender" class="form-select">
            <option value="">Select</option>
            <option>Male</option>
            <option>Female</option>
            <option>Other</option>
          </select>
        </div>
      </div>

      <div class="mb-2">
        <label class="form-label">Phone</label>
        <input v-model="form.phone" class="form-control" placeholder="Phone number" />
      </div>

      <div class="mb-3">
        <label class="form-label">Address</label>
        <textarea v-model="form.address" class="form-control" rows="2"
          placeholder="Address"></textarea>
      </div>

      <p v-if="err" class="text-danger small">{{ err }}</p>
      <p v-if="msg" class="text-success small">{{ msg }}</p>

      <button class="btn btn-success w-100" @click="register">Register</button>

      <p class="text-center mt-3 small">
        Already have an account?
        <router-link to="/login">Login here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      form: {
        name: '', email: '', password: '',
        age: '', gender: '', phone: '', address: ''
      },
      err: '',
      msg: ''
    }
  },
  methods: {
    async register() {
      this.err = ''
      this.msg = ''

      if (!this.form.name || !this.form.email || !this.form.password) {
        this.err = 'Name, email and password are required'
        return
      }

      try {
        const res = await axios.post('http://127.0.0.1:5000/api/register', this.form)
        this.msg = res.data.message
      } catch (e) {
        this.err = e.response?.data?.error || 'Registration failed'
      }
    }
  }
}
</script>
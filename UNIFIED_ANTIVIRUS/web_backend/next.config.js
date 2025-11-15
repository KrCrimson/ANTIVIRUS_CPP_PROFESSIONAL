/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    DATABASE_URL: process.env.DATABASE_URL,
    JWT_SECRET: process.env.JWT_SECRET,
    API_SECRET_KEY: process.env.API_SECRET_KEY,
  },
}

module.exports = nextConfig
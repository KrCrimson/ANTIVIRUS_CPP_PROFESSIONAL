const { PrismaClient } = require('@prisma/client')
const bcrypt = require('bcryptjs')

const prisma = new PrismaClient()

async function main() {
  console.log('🌱 Seeding database...')

  // Crear usuario admin por defecto
  const hashedPassword = await bcrypt.hash('admin123', 10)
  
  const adminUser = await prisma.user.upsert({
    where: { email: 'admin@unified-antivirus.com' },
    update: {},
    create: {
      email: 'admin@unified-antivirus.com',
      username: 'admin',
      password: hashedPassword,
      role: 'admin',
      isActive: true,
    },
  })

  console.log('👤 Admin user created:', adminUser.email)

  // Crear algunos clientes de ejemplo (opcional)
  const exampleClient = await prisma.antivirusClient.upsert({
    where: { clientId: 'example-client-001' },
    update: {},
    create: {
      clientId: 'example-client-001',
      hostname: 'example-workstation',
      version: '1.0.0',
      os: 'Windows 10 Pro',
      isActive: true,
    },
  })

  console.log('💻 Example client created:', exampleClient.hostname)

  console.log('✅ Database seeded successfully!')
}

main()
  .catch((e) => {
    console.error('❌ Error seeding database:', e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })
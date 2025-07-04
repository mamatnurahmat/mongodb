// Inisialisasi database dan user di MongoDB

// 1. Database mflix
const mflix = db.getSiblingDB('mflix');

// 2. User dengan akses readWrite ke mflix
mflix.createUser({
  user: 'mflix_rw',
  pwd: 'rw_password',
  roles: [{ role: 'readWrite', db: 'mflix' }]
});

// 3. User dengan akses read-only ke mflix
mflix.createUser({
  user: 'mflix_ro',
  pwd: 'ro_password',
  roles: [{ role: 'read', db: 'mflix' }]
});

// 4. User admin khusus mflix (dbAdmin + readWrite)
mflix.createUser({
  user: 'mflix_admin',
  pwd: 'admin_password',
  roles: [
    { role: 'dbAdmin', db: 'mflix' },
    { role: 'readWrite', db: 'mflix' }
  ]
}); 
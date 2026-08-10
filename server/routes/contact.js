const express = require('express');
const router = express.Router();

router.post('/', (req, res) => {
  const { name, email, message } = req.body;

  if (!name || !email || !message) {
    return res.status(400).json({ error: 'All fields are required' });
  }

  console.log('Contact form submission:');
  console.log(`  Name: ${name}`);
  console.log(`  Email: ${email}`);
  console.log(`  Message: ${message}`);
  console.log('---');

  res.json({ success: true, message: 'Message received' });
});

module.exports = router;

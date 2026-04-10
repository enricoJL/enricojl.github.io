#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const chokidar = require('chokidar');

const postsDir = path.join(__dirname, '../_posts');

// Créer le dossier scripts s'il n'existe pas
if (!fs.existsSync(path.join(__dirname))) {
  fs.mkdirSync(path.join(__dirname), { recursive: true });
}

console.log(`📁 Surveillance du dossier: ${postsDir}`);

chokidar.watch(postsDir, { ignored: /(^|[\/\\])\.|node_modules/ }).on('add', (filePath) => {
  if (!filePath.endsWith('.md')) return;

  setTimeout(() => {
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      
      // Vérifier si un front matter existe déjà
      if (content.trim().startsWith('---')) {
        console.log(`✓ ${path.basename(filePath)} a déjà un front matter`);
        return;
      }

      // Extraire la date et le titre du nom du fichier
      const filename = path.basename(filePath, '.md');
      const match = filename.match(/^(\d{4}-\d{2}-\d{2})-(.+)$/);
      
      if (!match) {
        console.log(`⚠️  ${filename} ne suit pas le format YYYY-MM-DD-titre`);
        return;
      }

      const [, dateStr, titleSlug] = match;
      const title = titleSlug.replace(/-/g, ' ');

      const frontMatter = `---
layout: post
title: "${title}"
date: "${dateStr}"
categories: "divers"
published: false
---
`;

      fs.writeFileSync(filePath, frontMatter + content);
      console.log(`✨ Front matter ajouté à ${filename}`);
    } catch (error) {
      console.error(`❌ Erreur: ${error.message}`);
    }
  }, 300); // Délai pour s'assurer que le fichier est complètement créé
});

console.log('⏳ Appuyer sur Ctrl+C pour arrêter');

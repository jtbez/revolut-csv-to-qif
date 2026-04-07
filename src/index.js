const { readFileSync, writeFileSync } = require('fs')
const { format } = require('date-fns')
const { resolve } = require('path')
const { EOL } = require('os')

const convert = require('./helpers/dif')

const ENCODING = 'utf8'

const file = resolve(process.argv[2])
const destDir = process.argv[3]

const buffer = readFileSync(file, ENCODING).split(EOL)
const data = convert(buffer)

const fileName = `Revolut-Statement-${format(new Date(), 'DD-MM-YYYY')}.qif`
const outputPath = destDir
  ? resolve(destDir, fileName)
  : resolve(process.cwd(), fileName)

writeFileSync(outputPath, ['!Type:Bank'].concat(data).join(EOL), { encoding: ENCODING })

const { parse } = require('date-fns')
const get = require('lodash.get')
const isEmpty = require('lodash.isempty')

const intlFormat = (n = '') => n.replace(',', '.')

const toNumber = str => {
  if (isEmpty(str))
    return '0.00'
  
  const num = parseFloat(intlFormat(str))
  return isNaN(num) ? '0.00' : num.toFixed(2)
}

const handleTransaction = operation => {
  const amount = get(operation, 'Amount', '0')

  if (parseFloat(amount) <= 0)
    return toNumber(amount)

  return `-${toNumber(amount)}`
}

module.exports = handleTransaction

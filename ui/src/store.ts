import { Writable, writable, derived, get } from 'svelte/store'

import type { TokenListType, TokenMetricsType, TokenSelectType } from './types/api.types'
import type { ToastMetaType } from './types/toast.types'
import { toBigNumber } from './utils'

export const saveStoreValue = (store, value) => {
  let currValue = JSON.stringify(get(store))
  let newValue = JSON.stringify(value)
  if (currValue !== newValue) store.set(value)
}

export const toast_store: Writable<ToastMetaType[]> = writable([])

export const lwc_info = writable({
  installed: null,
  locked: null,
  walletAddress: '',
  approved: false
})

export const mainMenuOpen = writable(false);
export const trollBoxOpen = writable(null);

export const walletBalance = writable(toBigNumber('0'))
export const tokenBalances = writable({})
export const lpBalances = writable({})
export const accountName = writable(null);
export const trollboxMessages = writable([]);
export const tradeHistory = writable([]);
export const tradeUpdates = writable([]);
export const bearerToken = writable(null)
export const keystore = writable(null);
export const lamdenWalletAutoConnect = writable(false);

export const rocketState = writable(0);

export const token_list_store: Writable<TokenListType[]> = writable([])
export const show_token_select_store: Writable<TokenSelectType> = writable({ open: false })
export const show_swap_confirm: Writable<boolean> = writable(false)
export const swap_confirm_loading: Writable<boolean> = writable(false)
export const ws_id: Writable<string> = writable('')

export const token_metrics_store: Writable<TokenMetricsType> = writable({})

export const walletAddress = derived([lwc_info, keystore], ([$lwc_info, $keystore]) => {
  if ($lwc_info?.approved && $lwc_info?.walletAddress) return $lwc_info?.walletAddress
  if ($keystore) return $keystore.wallets[0].vk
  return null
})

export const walletIsReady = derived([lwc_info, keystore], ([$lwc_info, $keystore]) => {
  console.log({lwc_info: $lwc_info, keystore: $keystore})
  console.log($keystore?.wallets?.length)
  if ($keystore?.wallets?.length > 0) return true
  return $lwc_info.installed === true && $lwc_info.locked === false && $lwc_info.approved === true && $lwc_info.walletAddress.length > 0
})
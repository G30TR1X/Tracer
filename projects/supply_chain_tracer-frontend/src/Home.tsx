// src/components/Home.tsx
import { useWallet } from '@txnlab/use-wallet-react'
import React, { useState } from 'react'
import ConnectWallet from './components/ConnectWallet'
import Transact from './components/Transact'
import AppCalls from './components/AppCalls'

interface HomeProps { }

const Home: React.FC<HomeProps> = () => {
  const [openWalletModal, setOpenWalletModal] = useState<boolean>(false)
  const [openDemoModal, setOpenDemoModal] = useState<boolean>(false)
  const [appCallsDemoModal, setAppCallsDemoModal] = useState<boolean>(false)
  const { activeAddress } = useWallet()

  const toggleWalletModal = () => {
    setOpenWalletModal(!openWalletModal)
  }

  const toggleDemoModal = () => {
    setOpenDemoModal(!openDemoModal)
  }

  const toggleAppCallsModal = () => {
    setAppCallsDemoModal(!appCallsDemoModal)
  }

  if (!activeAddress) {
    return (
      <div className="bg-white flex flex-col items-center justify-center min-h-screen">
        <p className="text-lg">
          Welcome to <strong>Tracer 🙂</strong>
        </p>
        <p className="">
          Connect to your wallet to get started!
        </p>

        <button data-test-id="connect-wallet" className="bg-teal-300 rounded-sm" onClick={toggleWalletModal}>
          Wallet Connection
        </button>

        <ConnectWallet openModal={openWalletModal} closeModal={toggleWalletModal} />
      </div>
    )
  }

  return (
    <div className=" bg-teal-400">
    </div>
  )

}

export default Home

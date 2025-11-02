from algopy import ARC4Contract, GlobalState, Global, BoxMap, Txn, Account, UInt64, Bytes
from algopy.arc4 import abimethod

class SupplyChainTracer(ARC4Contract):
    def __init__(self) -> None:
        # Track total registered batches
        self.total_batches = GlobalState(UInt64(0))

        # batch_id → serialized event string or hash
        self.batch_records = BoxMap(UInt64, Bytes)

        # batch_id → linked ASA id
        self.batch_assets = BoxMap(UInt64, UInt64)

        # authorized accounts that can write updates
        self.authorized = BoxMap(Account, UInt64)

    # -----------------------------
    # ADMIN / SETUP METHODS
    # -----------------------------

    @abimethod
    def authorize(self, account: Account) -> None:
        """
        Grant write permission to an account.
        Only the contract creator may do this.
        """
        assert Txn.sender == Global.creator_address, "Only creator can authorize"
        self.authorized[account] = UInt64(1)

    @abimethod
    def revoke(self, account: Account) -> None:
        """
        Remove write permission from an account.
        """
        assert Txn.sender == Global.creator_address, "Only creator can revoke"

        balance, admin = self.authorized.maybe(account)
        assert admin, "Account not authorized"

        del self.authorized[account]

    # -----------------------------
    # BATCH / SUPPLY CHAIN METHODS
    # -----------------------------

    @abimethod
    def register_batch(self, first_record: Bytes) -> UInt64:
        """
        Create a new batch entry.
        Assigns an incremental batch_id and stores initial metadata.
        """
        assert Txn.sender == Global.creator_address, "Only creator can register batches"
        batch_id = self.total_batches.value + UInt64(1)
        self.batch_records[batch_id] = first_record
        self.total_batches.value = batch_id
        return batch_id

    @abimethod
    def link_asset(self, batch_id: UInt64, asset_id: UInt64) -> None:
        """
        Link an ASA to a batch for tracking.
        Only the contract creator may do this.
        """
        assert Txn.sender == Global.creator_address, "Only creator can link assets"

        id, exists = self.batch_records.maybe(batch_id)
        assert exists, "Batch not found"

        self.batch_assets[batch_id] = asset_id

    @abimethod
    def record_event(self, batch_id: UInt64, new_data: Bytes) -> None:
        """
        Append a new record to an existing batch.
        Only authorized participants can call this.
        """
        balance, admin = self.authorized.maybe(Txn.sender)
        assert admin, "Unauthorized participant"

        old_data, exists = self.batch_records.maybe(batch_id)
        assert exists, "Batch not found"

        asset_id, asset_linked = self.batch_assets.maybe(batch_id)
        assert asset_linked, "No asset linked to this batch"

        # Concatenate new data to existing record string
        combined = old_data + b" | " + new_data
        self.batch_records[batch_id] = combined

    # -----------------------------
    # QUERY METHODS
    # -----------------------------

    @abimethod
    def get_batch_record(self, batch_id: UInt64) -> Bytes:
        """
        Return the full record string for a given batch.
        """
        record, exists = self.batch_records.maybe(batch_id)
        assert exists, "Batch not found"
        return record

    @abimethod
    def get_asset_for_batch(self, batch_id: UInt64) -> UInt64:
        """
        Return the linked ASA id for a given batch.
        """
        asset_id, exists = self.batch_assets.maybe(batch_id)
        assert exists, "No asset linked to this batch"
        return asset_id

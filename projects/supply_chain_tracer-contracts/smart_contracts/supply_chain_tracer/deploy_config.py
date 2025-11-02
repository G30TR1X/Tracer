import logging

import algokit_utils

logger = logging.getLogger(__name__)


# define deployment behaviour based on supplied app spec
def deploy() -> None:
    from smart_contracts.artifacts.supply_chain_tracer.supply_chain_tracer_client import (
        SupplyChainTracerFactory,
    )

    algorand = algokit_utils.AlgorandClient.from_environment()
    deployer_ = algorand.account.from_environment("DEPLOYER")

    # logger.info("Creating ASA for tracking...")
    # asa_result = algorand.send.asset_create(
    #     algokit_utils.AssetCreateParams(
    #         sender=deployer_.address,
    #         total=1_000_000,  # supply
    #         decimals=0,
    #         default_frozen=False,
    #         unit_name="TRC",
    #         asset_name="TracerBatchToken",
    #         url="https://tracer.app/asset",  # optional
    #         note=b"Tracer ASA for supply tracking",
    #     )
    # )
    # asa_id = asa_result.confirmation["asset-index"]
    # logger.info(f"Created ASA ID: {asa_id}")

    factory = algorand.client.get_typed_app_factory(
        SupplyChainTracerFactory, default_sender=deployer_.address
    )

    app_client, result = factory.deploy(
        on_update=algokit_utils.OnUpdate.AppendApp,
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
    )

    algorand.send.payment(
        algokit_utils.PaymentParams(
            amount=algokit_utils.AlgoAmount(algo=1),
            sender=deployer_.address,
            receiver=app_client.app_address,
        )
    )

    # logger.info("Registering first batch and linking ASA...")
    # batch_id = app_client.send.register_batch(first_record=b"Batch initialized")
    # app_client.send.link_asset(batch_id=batch_id.return_value, asset_id=asa_id)

    logger.info(
        f"Deployment complete: app_name={app_client.app_name} app_id=({app_client.app_id})"
    )

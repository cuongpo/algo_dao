# flake8: noqa
# fmt: off
# mypy: disable-error-code="no-any-return, no-untyped-call"
# This file was automatically generated by algokit-client-generator.
# DO NOT MODIFY IT BY HAND.
# requires: algokit-utils@^1.2.0
import base64
import dataclasses
import decimal
import typing
from abc import ABC, abstractmethod

import algokit_utils
import algosdk
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    AtomicTransactionResponse,
    TransactionSigner,
    TransactionWithSigner
)

_APP_SPEC_JSON = r"""{
    "hints": {
        "write_app_blob(uint64,string)void": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "get_app_state_val()string": {
            "call_config": {
                "no_op": "CALL"
            }
        }
    },
    "source": {
        "approval": "I3ByYWdtYSB2ZXJzaW9uIDgKaW50Y2Jsb2NrIDEyNyAwIDEKYnl0ZWNibG9jayAweCAweDAwMDEKdHhuIE51bUFwcEFyZ3MKaW50Y18xIC8vIDAKPT0KYm56IG1haW5fbDYKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMApwdXNoYnl0ZXMgMHhjMjIwMTI0OSAvLyAid3JpdGVfYXBwX2Jsb2IodWludDY0LHN0cmluZyl2b2lkIgo9PQpibnogbWFpbl9sNQp0eG5hIEFwcGxpY2F0aW9uQXJncyAwCnB1c2hieXRlcyAweGY0YzIyNTY2IC8vICJnZXRfYXBwX3N0YXRlX3ZhbCgpc3RyaW5nIgo9PQpibnogbWFpbl9sNAplcnIKbWFpbl9sNDoKdHhuIE9uQ29tcGxldGlvbgppbnRjXzEgLy8gTm9PcAo9PQp0eG4gQXBwbGljYXRpb25JRAppbnRjXzEgLy8gMAohPQomJgphc3NlcnQKY2FsbHN1YiBnZXRhcHBzdGF0ZXZhbGNhc3Rlcl83CmludGNfMiAvLyAxCnJldHVybgptYWluX2w1Ogp0eG4gT25Db21wbGV0aW9uCmludGNfMSAvLyBOb09wCj09CnR4biBBcHBsaWNhdGlvbklECmludGNfMSAvLyAwCiE9CiYmCmFzc2VydApjYWxsc3ViIHdyaXRlYXBwYmxvYmNhc3Rlcl82CmludGNfMiAvLyAxCnJldHVybgptYWluX2w2Ogp0eG4gT25Db21wbGV0aW9uCmludGNfMSAvLyBOb09wCj09CmJueiBtYWluX2w4CmVycgptYWluX2w4Ogp0eG4gQXBwbGljYXRpb25JRAppbnRjXzEgLy8gMAo9PQphc3NlcnQKY2FsbHN1YiBjcmVhdGVfMwppbnRjXzIgLy8gMQpyZXR1cm4KCi8vIHplcm9faW1wbAp6ZXJvaW1wbF8wOgpwcm90byAwIDAKaW50Y18wIC8vIDEyNwpiemVybwpwdXNoaW50IDIgLy8gMgoKICAgIHplcm9fbG9vcDoKICAgICAgICBpbnQgMQogICAgICAgIC0gICAgICAgICAgICAgICAvLyBbIjAwIipwYWdlX3NpemUsIGtleS0xXQogICAgICAgIGR1cDIgICAgICAgICAgICAvLyBbIjAwIipwYWdlX3NpemUsIGtleSwgIjAwIipwYWdlX3NpemUsIGtleV0KICAgICAgICBpdG9iICAgICAgICAgICAgLy8gWyIwMCIqcGFnZV9zaXplLCBrZXksICIwMCIqcGFnZV9zaXplLCBpdG9iKGtleSldCiAgICAgICAgZXh0cmFjdCA3IDEgICAgIC8vIFsiMDAiKnBhZ2Vfc2l6ZSwga2V5LCAiMDAiKnBhZ2Vfc2l6ZSwgaXRvYihrZXkpWy0xXV0KICAgICAgICBzd2FwICAgICAgICAgICAgLy8gWyIwMCIqcGFnZV9zaXplLCBrZXksIGl0b2Ioa2V5KVstMV0sICIwMCIqcGFnZV9zaXplXQogICAgICAgIGFwcF9nbG9iYWxfcHV0ICAvLyBbIjAwIipwYWdlX3NpemUsIGtleV0gIChyZW1vdmVzIHRvcCAyIGVsZW1lbnRzKQogICAgICAgIGR1cCAgICAgICAgICAgICAvLyBbIjAwIipwYWdlX3NpemUsIGtleS0xLCBrZXktMV0KICAgICAgICBibnogemVyb19sb29wICAgLy8gc3RhcnQgbG9vcCBvdmVyIGlmIGtleS0xPjAKICAgICAgICBwb3AKICAgICAgICBwb3AgICAgICAgICAgICAgLy8gdGFrZSBleHRyYSBqdW5rIG9mZiB0aGUgc3RhY2sKICAgICAgICByZXRzdWIKICAgIGNhbGxzdWIgemVyb19sb29wCiAgICAgICAgICAgIApyZXRzdWIKCi8vIHJlYWRfaW1wbApyZWFkaW1wbF8xOgpwcm90byAyIDEKYnl0ZWNfMCAvLyAiIgpzdG9yZSA2CmZyYW1lX2RpZyAtMgppbnRjXzAgLy8gMTI3Ci8Kc3RvcmUgNQpyZWFkaW1wbF8xX2wxOgpsb2FkIDUKZnJhbWVfZGlnIC0xCmludGNfMCAvLyAxMjcKLwo8PQpieiByZWFkaW1wbF8xX2w5CmxvYWQgNQpmcmFtZV9kaWcgLTIKaW50Y18wIC8vIDEyNwovCj09CmJueiByZWFkaW1wbF8xX2w4CmludGNfMSAvLyAwCnJlYWRpbXBsXzFfbDQ6CnN0b3JlIDcKbG9hZCA1CmZyYW1lX2RpZyAtMQppbnRjXzAgLy8gMTI3Ci8KPT0KYm56IHJlYWRpbXBsXzFfbDcKaW50Y18wIC8vIDEyNwpyZWFkaW1wbF8xX2w2OgpzdG9yZSA4CmxvYWQgNgpieXRlY18xIC8vIDB4MDAwMQpsb2FkIDUKaW50Y18yIC8vIDEKZXh0cmFjdDMKYXBwX2dsb2JhbF9nZXQKbG9hZCA3CmxvYWQgOApzdWJzdHJpbmczCmNvbmNhdApzdG9yZSA2CmxvYWQgNQppbnRjXzIgLy8gMQorCnN0b3JlIDUKYiByZWFkaW1wbF8xX2wxCnJlYWRpbXBsXzFfbDc6CmZyYW1lX2RpZyAtMQppbnRjXzAgLy8gMTI3CiUKYiByZWFkaW1wbF8xX2w2CnJlYWRpbXBsXzFfbDg6CmZyYW1lX2RpZyAtMgppbnRjXzAgLy8gMTI3CiUKYiByZWFkaW1wbF8xX2w0CnJlYWRpbXBsXzFfbDk6CmxvYWQgNgpyZXRzdWIKCi8vIHdyaXRlX2ltcGwKd3JpdGVpbXBsXzI6CnByb3RvIDIgMAppbnRjXzEgLy8gMApzdG9yZSAzCmZyYW1lX2RpZyAtMgppbnRjXzAgLy8gMTI3Ci8Kc3RvcmUgMAp3cml0ZWltcGxfMl9sMToKbG9hZCAwCmZyYW1lX2RpZyAtMgpmcmFtZV9kaWcgLTEKbGVuCisKaW50Y18wIC8vIDEyNwovCjw9CmJ6IHdyaXRlaW1wbF8yX2wxMgpsb2FkIDAKZnJhbWVfZGlnIC0yCmludGNfMCAvLyAxMjcKLwo9PQpibnogd3JpdGVpbXBsXzJfbDExCmludGNfMSAvLyAwCndyaXRlaW1wbF8yX2w0OgpzdG9yZSAxCmxvYWQgMApmcmFtZV9kaWcgLTIKZnJhbWVfZGlnIC0xCmxlbgorCmludGNfMCAvLyAxMjcKLwo9PQpibnogd3JpdGVpbXBsXzJfbDEwCmludGNfMCAvLyAxMjcKd3JpdGVpbXBsXzJfbDY6CnN0b3JlIDIKYnl0ZWNfMSAvLyAweDAwMDEKbG9hZCAwCmludGNfMiAvLyAxCmV4dHJhY3QzCmxvYWQgMgppbnRjXzAgLy8gMTI3CiE9CmxvYWQgMQppbnRjXzEgLy8gMAohPQp8fApibnogd3JpdGVpbXBsXzJfbDkKaW50Y18wIC8vIDEyNwpzdG9yZSA0CmZyYW1lX2RpZyAtMQpsb2FkIDMKaW50Y18wIC8vIDEyNwpleHRyYWN0Mwp3cml0ZWltcGxfMl9sODoKYXBwX2dsb2JhbF9wdXQKbG9hZCAzCmxvYWQgNAorCnN0b3JlIDMKbG9hZCAwCmludGNfMiAvLyAxCisKc3RvcmUgMApiIHdyaXRlaW1wbF8yX2wxCndyaXRlaW1wbF8yX2w5Ogpsb2FkIDIKbG9hZCAxCi0Kc3RvcmUgNApieXRlY18xIC8vIDB4MDAwMQpsb2FkIDAKaW50Y18yIC8vIDEKZXh0cmFjdDMKYXBwX2dsb2JhbF9nZXQKaW50Y18xIC8vIDAKbG9hZCAxCnN1YnN0cmluZzMKZnJhbWVfZGlnIC0xCmxvYWQgMwpsb2FkIDQKZXh0cmFjdDMKY29uY2F0CmJ5dGVjXzEgLy8gMHgwMDAxCmxvYWQgMAppbnRjXzIgLy8gMQpleHRyYWN0MwphcHBfZ2xvYmFsX2dldApsb2FkIDIKaW50Y18wIC8vIDEyNwpzdWJzdHJpbmczCmNvbmNhdApiIHdyaXRlaW1wbF8yX2w4CndyaXRlaW1wbF8yX2wxMDoKZnJhbWVfZGlnIC0yCmZyYW1lX2RpZyAtMQpsZW4KKwppbnRjXzAgLy8gMTI3CiUKYiB3cml0ZWltcGxfMl9sNgp3cml0ZWltcGxfMl9sMTE6CmZyYW1lX2RpZyAtMgppbnRjXzAgLy8gMTI3CiUKYiB3cml0ZWltcGxfMl9sNAp3cml0ZWltcGxfMl9sMTI6CnJldHN1YgoKLy8gY3JlYXRlCmNyZWF0ZV8zOgpwcm90byAwIDAKY2FsbHN1YiB6ZXJvaW1wbF8wCnJldHN1YgoKLy8gd3JpdGVfYXBwX2Jsb2IKd3JpdGVhcHBibG9iXzQ6CnByb3RvIDIgMApmcmFtZV9kaWcgLTIKZnJhbWVfZGlnIC0xCmV4dHJhY3QgMiAwCmNhbGxzdWIgd3JpdGVpbXBsXzIKcmV0c3ViCgovLyBnZXRfYXBwX3N0YXRlX3ZhbApnZXRhcHBzdGF0ZXZhbF81Ogpwcm90byAwIDEKYnl0ZWNfMCAvLyAiIgppbnRjXzEgLy8gMApwdXNoaW50IDI1NCAvLyAyNTQKaW50Y18yIC8vIDEKLQpjYWxsc3ViIHJlYWRpbXBsXzEKZnJhbWVfYnVyeSAwCmZyYW1lX2RpZyAwCmxlbgppdG9iCmV4dHJhY3QgNiAwCmZyYW1lX2RpZyAwCmNvbmNhdApmcmFtZV9idXJ5IDAKcmV0c3ViCgovLyB3cml0ZV9hcHBfYmxvYl9jYXN0ZXIKd3JpdGVhcHBibG9iY2FzdGVyXzY6CnByb3RvIDAgMAppbnRjXzEgLy8gMApieXRlY18wIC8vICIiCnR4bmEgQXBwbGljYXRpb25BcmdzIDEKYnRvaQpmcmFtZV9idXJ5IDAKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMgpmcmFtZV9idXJ5IDEKZnJhbWVfZGlnIDAKZnJhbWVfZGlnIDEKY2FsbHN1YiB3cml0ZWFwcGJsb2JfNApyZXRzdWIKCi8vIGdldF9hcHBfc3RhdGVfdmFsX2Nhc3RlcgpnZXRhcHBzdGF0ZXZhbGNhc3Rlcl83Ogpwcm90byAwIDAKYnl0ZWNfMCAvLyAiIgpjYWxsc3ViIGdldGFwcHN0YXRldmFsXzUKZnJhbWVfYnVyeSAwCnB1c2hieXRlcyAweDE1MWY3Yzc1IC8vIDB4MTUxZjdjNzUKZnJhbWVfZGlnIDAKY29uY2F0CmxvZwpyZXRzdWI=",
        "clear": "I3ByYWdtYSB2ZXJzaW9uIDgKcHVzaGludCAwIC8vIDAKcmV0dXJu"
    },
    "state": {
        "global": {
            "num_byte_slices": 2,
            "num_uints": 0
        },
        "local": {
            "num_byte_slices": 0,
            "num_uints": 0
        }
    },
    "schema": {
        "global": {
            "declared": {},
            "reserved": {}
        },
        "local": {
            "declared": {},
            "reserved": {}
        }
    },
    "contract": {
        "name": "Global Blob App",
        "methods": [
            {
                "name": "write_app_blob",
                "args": [
                    {
                        "type": "uint64",
                        "name": "start"
                    },
                    {
                        "type": "string",
                        "name": "v"
                    }
                ],
                "returns": {
                    "type": "void"
                }
            },
            {
                "name": "get_app_state_val",
                "args": [],
                "returns": {
                    "type": "string"
                }
            }
        ],
        "networks": {}
    },
    "bare_call_config": {
        "no_op": "CREATE"
    }
}"""
APP_SPEC = algokit_utils.ApplicationSpecification.from_json(_APP_SPEC_JSON)
_TReturn = typing.TypeVar("_TReturn")


class _ArgsBase(ABC, typing.Generic[_TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ...


_TArgs = typing.TypeVar("_TArgs", bound=_ArgsBase[typing.Any])


@dataclasses.dataclass(kw_only=True)
class _TArgsHolder(typing.Generic[_TArgs]):
    args: _TArgs


def _filter_none(value: dict | typing.Any) -> dict | typing.Any:
    if isinstance(value, dict):
        return {k: _filter_none(v) for k, v in value.items() if v is not None}
    return value


def _as_dict(data: typing.Any, *, convert_all: bool = True) -> dict[str, typing.Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    if convert_all:
        result = dataclasses.asdict(data)
    else:
        result = {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}
    return _filter_none(result)


def _convert_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.TransactionParametersDict:
    return typing.cast(algokit_utils.TransactionParametersDict, _as_dict(transaction_parameters))


def _convert_call_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.OnCompleteCallParametersDict:
    return typing.cast(algokit_utils.OnCompleteCallParametersDict, _as_dict(transaction_parameters))


def _convert_create_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
    on_complete: algokit_utils.OnCompleteActionName,
) -> algokit_utils.CreateCallParametersDict:
    result = typing.cast(algokit_utils.CreateCallParametersDict, _as_dict(transaction_parameters))
    on_complete_enum = on_complete.replace("_", " ").title().replace(" ", "") + "OC"
    result["on_complete"] = getattr(algosdk.transaction.OnComplete, on_complete_enum)
    return result


def _convert_deploy_args(
    deploy_args: algokit_utils.DeployCallArgs | None,
) -> algokit_utils.ABICreateCallArgsDict | None:
    if deploy_args is None:
        return None

    deploy_args_dict = typing.cast(algokit_utils.ABICreateCallArgsDict, _as_dict(deploy_args))
    if isinstance(deploy_args, _TArgsHolder):
        deploy_args_dict["args"] = _as_dict(deploy_args.args)
        deploy_args_dict["method"] = deploy_args.args.method()

    return deploy_args_dict


@dataclasses.dataclass(kw_only=True)
class WriteAppBlobArgs(_ArgsBase[None]):
    start: int
    v: str

    @staticmethod
    def method() -> str:
        return "write_app_blob(uint64,string)void"


@dataclasses.dataclass(kw_only=True)
class GetAppStateValArgs(_ArgsBase[str]):
    @staticmethod
    def method() -> str:
        return "get_app_state_val()string"


class Composer:

    def __init__(self, app_client: algokit_utils.ApplicationClient, atc: AtomicTransactionComposer):
        self.app_client = app_client
        self.atc = atc

    def build(self) -> AtomicTransactionComposer:
        return self.atc

    def execute(self) -> AtomicTransactionResponse:
        return self.app_client.execute_atc(self.atc)

    def write_app_blob(
        self,
        *,
        start: int,
        v: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `write_app_blob(uint64,string)void` ABI method
        
        :param int start: The `start` ABI parameter
        :param str v: The `v` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = WriteAppBlobArgs(
            start=start,
            v=v,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def get_app_state_val(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `get_app_state_val()string` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = GetAppStateValArgs()
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def create_bare(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to create an application using the no_op bare method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        self.app_client.compose_create(
            self.atc,
            call_abi_method=False,
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
        )
        return self

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> "Composer":
        """Adds a call to the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass"""
    
        self.app_client.compose_clear_state(self.atc, _convert_transaction_parameters(transaction_parameters), app_args)
        return self


class GlobalBlobAppClient:
    """A class for interacting with the Global Blob App app providing high productivity and
    strongly typed methods to deploy and call the app"""

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account | None = None,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        """
        GlobalBlobAppClient can be created with an app_id to interact with an existing application, alternatively
        it can be created with a creator and indexer_client specified to find existing applications by name and creator.
        
        :param AlgodClient algod_client: AlgoSDK algod client
        :param int app_id: The app_id of an existing application, to instead find the application by creator and name
        use the creator and indexer_client parameters
        :param str | Account creator: The address or Account of the app creator to resolve the app_id
        :param IndexerClient indexer_client: AlgoSDK indexer client, only required if deploying or finding app_id by
        creator and app name
        :param AppLookup existing_deployments:
        :param TransactionSigner | Account signer: Account or signer to use to sign transactions, if not specified and
        creator was passed as an Account will use that.
        :param str sender: Address to use as the sender for all transactions, will use the address associated with the
        signer if not specified.
        :param TemplateValueMapping template_values: Values to use for TMPL_* template variables, dictionary keys should
        *NOT* include the TMPL_ prefix
        :param str | None app_name: Name of application to use when deploying, defaults to name defined on the
        Application Specification
            """

        self.app_spec = APP_SPEC
        
        # calling full __init__ signature, so ignoring mypy warning about overloads
        self.app_client = algokit_utils.ApplicationClient(  # type: ignore[call-overload, misc]
            algod_client=algod_client,
            app_spec=self.app_spec,
            app_id=app_id,
            creator=creator,
            indexer_client=indexer_client,
            existing_deployments=existing_deployments,
            signer=signer,
            sender=sender,
            suggested_params=suggested_params,
            template_values=template_values,
            app_name=app_name,
        )

    @property
    def algod_client(self) -> algosdk.v2client.algod.AlgodClient:
        return self.app_client.algod_client

    @property
    def app_id(self) -> int:
        return self.app_client.app_id

    @app_id.setter
    def app_id(self, value: int) -> None:
        self.app_client.app_id = value

    @property
    def app_address(self) -> str:
        return self.app_client.app_address

    @property
    def sender(self) -> str | None:
        return self.app_client.sender

    @sender.setter
    def sender(self, value: str) -> None:
        self.app_client.sender = value

    @property
    def signer(self) -> TransactionSigner | None:
        return self.app_client.signer

    @signer.setter
    def signer(self, value: TransactionSigner) -> None:
        self.app_client.signer = value

    @property
    def suggested_params(self) -> algosdk.transaction.SuggestedParams | None:
        return self.app_client.suggested_params

    @suggested_params.setter
    def suggested_params(self, value: algosdk.transaction.SuggestedParams | None) -> None:
        self.app_client.suggested_params = value

    def write_app_blob(
        self,
        *,
        start: int,
        v: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Calls `write_app_blob(uint64,string)void` ABI method
        
        :param int start: The `start` ABI parameter
        :param str v: The `v` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[None]: The result of the transaction"""

        args = WriteAppBlobArgs(
            start=start,
            v=v,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def get_app_state_val(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Calls `get_app_state_val()string` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[str]: The result of the transaction"""

        args = GetAppStateValArgs()
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def create_bare(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Creates an application using the no_op bare method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.TransactionResponse: The result of the transaction"""

        result = self.app_client.create(
            call_abi_method=False,
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
        )
        return result

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Calls the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass
        :returns algokit_utils.TransactionResponse: The result of the transaction"""
    
        return self.app_client.clear_state(_convert_transaction_parameters(transaction_parameters), app_args)

    def deploy(
        self,
        version: str | None = None,
        *,
        signer: TransactionSigner | None = None,
        sender: str | None = None,
        allow_update: bool | None = None,
        allow_delete: bool | None = None,
        on_update: algokit_utils.OnUpdate = algokit_utils.OnUpdate.Fail,
        on_schema_break: algokit_utils.OnSchemaBreak = algokit_utils.OnSchemaBreak.Fail,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        create_args: algokit_utils.DeployCallArgs | None = None,
        update_args: algokit_utils.DeployCallArgs | None = None,
        delete_args: algokit_utils.DeployCallArgs | None = None,
    ) -> algokit_utils.DeployResponse:
        """Deploy an application and update client to reference it.
        
        Idempotently deploy (create, update/delete if changed) an app against the given name via the given creator
        account, including deploy-time template placeholder substitutions.
        To understand the architecture decisions behind this functionality please see
        <https://github.com/algorandfoundation/algokit-cli/blob/main/docs/architecture-decisions/2023-01-12_smart-contract-deployment.md>
        
        ```{note}
        If there is a breaking state schema change to an existing app (and `on_schema_break` is set to
        'ReplaceApp' the existing app will be deleted and re-created.
        ```
        
        ```{note}
        If there is an update (different TEAL code) to an existing app (and `on_update` is set to 'ReplaceApp')
        the existing app will be deleted and re-created.
        ```
        
        :param str version: version to use when creating or updating app, if None version will be auto incremented
        :param algosdk.atomic_transaction_composer.TransactionSigner signer: signer to use when deploying app
        , if None uses self.signer
        :param str sender: sender address to use when deploying app, if None uses self.sender
        :param bool allow_delete: Used to set the `TMPL_DELETABLE` template variable to conditionally control if an app
        can be deleted
        :param bool allow_update: Used to set the `TMPL_UPDATABLE` template variable to conditionally control if an app
        can be updated
        :param OnUpdate on_update: Determines what action to take if an application update is required
        :param OnSchemaBreak on_schema_break: Determines what action to take if an application schema requirements
        has increased beyond the current allocation
        :param dict[str, int|str|bytes] template_values: Values to use for `TMPL_*` template variables, dictionary keys
        should *NOT* include the TMPL_ prefix
        :param algokit_utils.DeployCallArgs | None create_args: Arguments used when creating an application
        :param algokit_utils.DeployCallArgs | None update_args: Arguments used when updating an application
        :param algokit_utils.DeployCallArgs | None delete_args: Arguments used when deleting an application
        :return DeployResponse: details action taken and relevant transactions
        :raises DeploymentError: If the deployment failed"""

        return self.app_client.deploy(
            version,
            signer=signer,
            sender=sender,
            allow_update=allow_update,
            allow_delete=allow_delete,
            on_update=on_update,
            on_schema_break=on_schema_break,
            template_values=template_values,
            create_args=_convert_deploy_args(create_args),
            update_args=_convert_deploy_args(update_args),
            delete_args=_convert_deploy_args(delete_args),
        )

    def compose(self, atc: AtomicTransactionComposer | None = None) -> Composer:
        return Composer(self.app_client, atc or AtomicTransactionComposer())

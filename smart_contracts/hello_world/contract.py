from beaker import *
from pyteal import *

from beaker.lib.storage import BoxMapping


class proposalStruct(abi.NamedTuple):
    description: abi.Field[abi.String]
    vote_yes: abi.Field[abi.Uint64]
    vote_no: abi.Field[abi.Uint64]
    status: abi.Field[abi.String]


class AppStateValue:
    memberCount = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Number Member of DAO",
    )

    proposalCount = GlobalStateValue(
        stack_type=TealType.uint64, default=Int(0), descr="Number of Proposals"
    )

    memberDAO = LocalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Member DAO or not",
    )

    check_voted = ReservedLocalStateValue(
        stack_type=TealType.uint64,
        max_keys=8,
        descr=("Check user voted in proposal"),
    )

    proposals = BoxMapping(abi.Uint64, proposalStruct)


app = (
    Application("Simple DAO", state=AppStateValue())
    .apply(unconditional_create_approval, initialize_global_state=True)
    .apply(unconditional_opt_in_approval, initialize_local_state=True)
)


## Check member dao or not
@app.external
def check_member_dao(*, output: abi.Uint64) -> Expr:
    return output.set(app.state.memberDAO[Txn.sender()])


## Join DAO
@app.external
def join_dao() -> Expr:
    return Seq(
        app.state.memberDAO[Txn.sender()].set(Int(1)),
        app.state.memberCount.increment(),
    )


## Leave DAO
@app.external
def leave_dao() -> Expr:
    return Seq(
        app.state.memberDAO[Txn.sender()].set(Int(1)),
        app.state.memberCount.decrement(),
    )


## Create Proposal
@app.external
def create_proposal(descr: abi.String, *, output: proposalStruct) -> Expr:
    proposal_tuple = proposalStruct()
    proposalId = abi.Uint64()
    vote_yes = abi.Uint64()
    vote_no = abi.Uint64()
    status = abi.String()
    return Seq(
        vote_yes.set(Int(0)),
        vote_no.set(Int(0)),
        status.set("In Progress"),
        proposal_tuple.set(descr, vote_yes, vote_no, status),
        proposalId.set(app.state.proposalCount.get()),
        app.state.proposals[proposalId].set(proposal_tuple),
        app.state.proposalCount.increment(),
        app.state.proposals[proposalId].store_into(output),
    )


## Check Proposal
@app.external
def check_proposal(proposalId: abi.Uint64, *, output: proposalStruct) -> Expr:
    return app.state.proposals[proposalId].store_into(output)


## End Proposal when total vote > 1/2 member Count
@app.external
def end_proposal(proposalId: abi.Uint64, *, output: abi.String) -> Expr:
    proposal = proposalStruct()
    description = abi.String()
    vote_yes = abi.Uint64()
    vote_no = abi.Uint64()
    status = abi.String()
    new_status = abi.String()

    total_dao_member = app.state.memberCount.get()
    app.state.proposals[proposalId].store_into(proposal)
    description.set(proposal.description)
    vote_yes.set(proposal.vote_yes)
    vote_no.set(proposal.vote_no)
    status.set(proposal.status)

    if status != "In Progress":
        return output.set("Proposal Ended")

    if 2 * (vote_yes + vote_no) < total_dao_member:
        return output.set("not enough vote")

    if vote_yes < vote_no:
        return Seq(
            output.set("proposal failed"),
            new_status.set("proposal failed"),
            proposal.set(description, vote_yes, vote_no, new_status),
            app.state.proposals[proposalId].set(proposal),
        )

    return Seq(
        output.set("proposal success"),
        new_status.set("proposal success"),
        proposal.set(description, vote_yes, vote_no, new_status),
        app.state.proposals[proposalId].set(proposal),
    )


## Vote yes=true, no=false
@app.external
def vote(proposalId: abi.Uint64, vote_choice: abi.Bool, *, output: abi.String) -> Expr:
    voted = abi.Uint64()
    proposal = proposalStruct()
    description = abi.String()
    vote_yes = abi.Uint64()
    vote_no = abi.Uint64()
    status = abi.String()

    voted.set(app.state.check_voted[proposalId])

    if voted.get() == Int(1):
        output.set("you voted ----")

    app.state.proposals[proposalId].store_into(proposal)
    description.set(proposal.description)
    status.set(proposal.status)
    vote_yes.set(proposal.vote_yes)
    vote_no.set(proposal.vote_no)

    if vote_choice:
        vote_yes.set(vote_yes.get() + Int(1))
    else:
        vote_no.set(vote_no.get() + Int(1))

    return Seq(
        proposal.set(description, vote_yes, vote_no, status),
        app.state.proposals[proposalId].set(proposal),
        app.state.check_voted[proposalId].set(Int(1)),
        output.set("Vote Successfully"),
    )


@app.external
def check_voted(proposalId: abi.Uint64, *, output: abi.Uint64) -> Expr:
    return output.set(app.state.check_voted[proposalId])

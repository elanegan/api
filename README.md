# Premiere Protocol API

[![License](https://img.shields.io/github/license/piotrostr/premiere-api?color=blue)](https://github.com/piotrostr/premiere-api/blob/master/LICENSE)
![Test](https://github.com/piotrostr/premiere-api/actions/workflows/main.yml/badge.svg)
[![codecov](https://codecov.io/gh/piotrostr/premiere-api/branch/master/graph/badge.svg?token=WZMNTI0JJN)](https://codecov.io/gh/piotrostr/premiere-api)
[![CodeFactor](https://www.codefactor.io/repository/github/piotrostr/premiere-api/badge/master)](https://www.codefactor.io/repository/github/piotrostr/premiere-api/overview/master)

## Usage

[Docs](https://api.premiere.sh/docs) (OpenAPI format)

## Development

Create `.env` file with contents:

```sh
POSTGRES_USERNAME=postgres
POSTGRES_PASSWORD=pw
POSTGRES_HOST=db
```

In order to run tests:

```sh
docker-compose run api pytest --cov=. --cov-report=html
```

## Contributing

See [CONTRIBUTING.md](https://github.com/premiere-sh/api/blob/master/CONTRIBUTING.md)

## Business Logic

<table>
  <tbody>
    <tr>
      <td>The ability to set up an account using an email</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Tournament CRUD</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>The ability to deposit fiat through Stripe or Crypto</td>
      <td></td>
    </tr>
    <tr>
      <td>
        Take credit off users accounts on joining tounaments, pay out winnings
      </td>
      <td></td>
    </tr>
    <tr>
      <td>
        Send out notifications to users when tournaments are created with unique
        code to join
      </td>
      <td></td>
    </tr>
    <tr>
      <td>
        Most popular tournament on stream on the home page of each game
      </td>
      <td></td>
    </tr>
    <tr>
      <td>
        player of the week endpoint - most tournmanets won
      </td>
      <td></td>
    </tr>
    <tr>
      <td>Ability to withdraw</td>
      <td></td>
    </tr>
    <tr>
      <td>Ability to play in teams and add friends</td>
      <td></td>
    </tr>
  </tbody>
</table>

### Additional Remarks

Games are going to be fixed and added based on the business needs,
warzone is going to be the first implementation. At first there will only be
one platform, probably cross-play stemming from battle.net

If it would end up being crypto-based, there could be a L2 Arbitrum smart
contract to keep track of everything safely on chain.

Below are some loose thoughts from previous meetings with the stakeholders.

```solidity
contract Premiere {

    // this would probably require merkle proofs for checking the players

    struct Tournament {
        uint entryPrice;
        uint currentPlayerId;
        uint startDate;
        uint playerCap;
        uint winnerAddress;
    }

    mapping(uint => Tournament) public tournaments;

    function joinTournament(uint tournamentId) {
        Tournament tournament = tournaments[tournamentId];
        require(tournament.currentPlayerId < tournament.playerCap);
        // ...
    }

    function finalise(Tournament t, address winner) external onlyAuthorized {
        // withdraw(winnerAddress);
        // withdraw to the winner, write the tournament as done
    }

    function getBestPlayer() external view {
        // storage is quite expensive, but a function that loops through
        // and only reads could be very cheap computation-wise
    }
}
```

## Stack

FastAPI with PostgreSQL database, with user authentication and endpoints for
CRUD operations on tournaments and games. Running on Terraform-provisioned
Linode Kubernetes Engine cluster with NGINX node balancing with TLS.

## Deployment

### Networking

After provisioning with terraform (requires the `terraform.tfvars` file) and
getting the `kubeconfig.yml`, let's expose the cluster with an ingress:

```sh
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace
```

Then get the ipv4 of the ingress and point the domain (in this case
`api.premiere.sh`) to it. Note that the hostname has to be included in the
`manifest.yml`. Next, get cert:

```sh
kubectl apply -f \
  https://github.com/cert-manager/cert-manager/releases/download/v1.8.0/cert-manager.yaml
```

This should leave to `api.premiere.sh` being accessible both via `HTTP/HTTPS`
and returning 503 status from nginx.

### Services

Having exposed the cluster, deploy the resorces.

`.env` file contents:

```sh
POSTGRES_USERNAME=***
POSTGRES_PASSWORD=***
POSTGRES_HOST=***
```

```bash
kubectl create secret generic premiere-secrets --from-env-file=./.env
```

```sh
kubectl apply -f manifest.yml
```

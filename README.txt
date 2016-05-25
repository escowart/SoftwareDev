Evolution Board Game implement in python


Authors: Edwin Cowart, Beatrice Huang


Run a server and client for the full Evolution Game, xall_tests to run all tests.

Running this program:
  ./server              : Runs Server for the Evolution Game
  ./client              : Runs Client for the Evolution Game
  ./xall_tests          : Runs all unit and integration tests
  ./server_with_clients : Runs a Server with a number of Client Threads
  ./old_exe.main        : Runs Evolution Game

Evolution structure:
    run_server_and_client
    run_evolution_server      @sever.py                                   : Run the Evolution Server
    Dealer                    @evolution.dealers.dealer                   : The Dealer of the Game
        - run_evolution                                                   : Runs the Evolution Game
            - is_game_over                                                : Checks for Game Over conditions
            - step1                                                       : Step 1 of the Evolution Game
            - step2_and_step3                                             : Step 2 and Step 3 of the Evolution Game
            - step4                                                       : Step 4 of the Evolution Game
            - end_game                                                    : Runs the End Game print out
    PlayerSequence            @evolution.dealers.player_sequence          : The Sequence of Players in the order
    Player                    @evolution.player.player                    : A Player of the Game
    ExternalPlayer            @evolution.external_players.external_player : The External Player Interface
    ProxyPlayer               @evolution.external_players.proxy_player    : An External Player for interacting with a
                                                                          :  Client
    MessageSocket             @evolution.messages.message_socket          : A Message socket for 2-way communication
    Message                   @evolution.messages.message                 : A Message to/from Proxies
    WateringHole              @evolution.card_holders.watering_hole       : The watering hole of the Game
    Deck                      @evolution.card_holders.deck                : The deck of cards
    Species                   @evolution.species.species                  : A Species in the Game
    TraitCard                 @evolution.cards.trait_cards                : A Trait Card of a Species

    run_evolution_client      @client.py                                  : Runs the Evolution Client during setup
    ProxyDealer               @evolution.dealers.proxy_dealer             : Runs the Evolution Client after setup
        - run_evolution_for_client                                        : Runs the Client side Evolution Game
    ClientPlayer              @evolution.dealers.proxy_dealer             : The Player of the Client
    SillyPlayer               @evolution.external_players.silly_player    : The Silly Player Strategy


import DAG for evolution package:
    -> Root Evo   (all_root_evo)
    -> Interfaces (all_interfaces)
    -> TraitCards
    -> CardHolders
    -> Species
    -> Messages
    -> ExternalPlayers
    -> Player
    -> PlayerSequence
    -> Dealers    (all_evo)


GUI structure:
  ImageGenerator               @gui.base_generators.image_gen             : Displays on a tk.Canvas
  BasicIGen                    @gui.base_generators.basic_gen             : Displays using tk.Canvas.create_...
  ComplexIGen                  @gui.base_generators.complex_gen           : IGen which displays multiple other IGens

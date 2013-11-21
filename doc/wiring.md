                          ╭───────────────────────────────────────────────────────────────╮
			  │    FlopPi-Music Wiring Diagram - Draft for 8 Floppy Drives    │
                          │           © 2013 Dominik George, Eike Tim Jesinghaus          │
                          │ Published under the terms and conditions of The MirOS Licence │
                          ╰───────────────────────────────────────────────────────────────╯

   3½″ IBM-PC Floppy Drive Pin-Out                    Raspberry Pi                 3½″ IBM-PC Floppy Drive Pin-Out
             Drives 0 - 3                              Rev 1 GPIO                            Drives 4 - 7

                   ┌───────────────────────────────────┐       ┌─────────────────────────────────────┐
                   │ ┌────────────────────────────────┐│       │┌──────────────────────────────────┐ │
 2                 │ │              34                ││       ││                2                 │ │              34
 ┏━━━━━━━━━━━━━━━━━┿━┿━━━━━━━━━━━━━━━┓                ││       ││                ┏━━━━━━━━━━━━━━━━━┿━┿━━━━━━━━━━━━━━━┓
 ┃ · · · · · ╮ · · ╵ ╵ · · · · · · · ┃                ││       ││                ┃ · · · · · ╮ · · ╵ ╵ · · · · · · · ┃
 ┃ · · · · · ╯ · · ╷ ╷ · · · · · · · ┃                ││       ││                ┃ · · · · · ╯ · · ╷ ╷ · · · · · · · ┃
 ┗━━━━━━━━━━━━━━━━━┿━┿━━━━━━━━━━━━━━━┛                ││       ││                ┗━━━━━━━━━━━━━━━━━┿━┿━━━━━━━━━━━━━━━┛
 1                 └┬┘              33                ││       ││                1                 └┬┘              33
                    ⏚                                 ││       ││                                   ⏚
                   ┌─────────────────────────────────┐││1     2││┌───────────────────────────────────┐
                   │ ┌──────────────────────────────┐│││┏━━━━━┓│││┌────────────────────────────────┐ │
 2                 │ │              34              ││││┃ · · ┃││││              2                 │ │              34
 ┏━━━━━━━━━━━━━━━━━┿━┿━━━━━━━━━━━━━━━┓              │││└╂─╴ · ┃││││              ┏━━━━━━━━━━━━━━━━━┿━┿━━━━━━━━━━━━━━━┓
 ┃ · · · · · ╮ · · ╵ ╵ · · · · · · · ┃              ││└─╂─╴ · ┃││││              ┃ · · · · · ╮ · · ╵ ╵ · · · · · · · ┃
 ┃ · · · · · ╯ · · ╷ ╷ · · · · · · · ┃              ││  ┃ · ╶─╂┘│││              ┃ · · · · · ╯ · · ╷ ╷ · · · · · · · ┃
 ┗━━━━━━━━━━━━━━━━━┿━┿━━━━━━━━━━━━━━━┛              ││  ┃ · ╶─╂─┘││              ┗━━━━━━━━━━━━━━━━━┿━┿━━━━━━━━━━━━━━━┛
 1                 └┬┘              33              │└──╂─╴ ╶─╂──┘│              1                 └┬┘              33
                    ⏚                               └───╂─╴ · ┃   │                                 ⏚
                   ┌────────────────────────────────────╂─╴ ╶─╂───┘┌─────────────────────────────────┐
                   │ ┌───────────────────────────────┐  ┃ · ╶─╂────┘┌──────────────────────────────┐ │
 2                 │ │              34               └──╂─╴┌╴ ┃     │            2                 │ │              34
 ┏━━━━━━━━━━━━━━━━━┿━┿━━━━━━━━━━━━━━━┓                ┌─╂─╴│╶─╂─────┘            ┏━━━━━━━━━━━━━━━━━┿━┿━━━━━━━━━━━━━━━┓
 ┃ · · · · · ╮ · · ╵ ╵ · · · · · · · ┃                │┌╂─╴│╶─╂─┐                ┃ · · · · · ╮ · · ╵ ╵ · · · · · · · ┃
 ┃ · · · · · ╯ · · ╷ ╷ · · · · · · · ┃                ││┃ ·│╶─╂┐│                ┃ · · · · · ╯ · · ╷ ╷ · · · · · · · ┃
 ┗━━━━━━━━━━━━━━━━━┿━┿━━━━━━━━━━━━━━━┛                ││┗━━┿━━┛││                ┗━━━━━━━━━━━━━━━━━┿━┿━━━━━━━━━━━━━━━┛
 1                 └┬┘              33                ││25 │ 26││                1                 └┬┘              33
                    ⏚                                 ││   ⏚   ││                                   ⏚
                   ┌──────────────────────────────────┘│       │└────────────────────────────────────┐
                   │ ┌─────────────────────────────────┘       └───────────────────────────────────┐ │
 2                 │ │              34                                           2                 │ │              34
 ┏━━━━━━━━━━━━━━━━━┿━┿━━━━━━━━━━━━━━━┓          ╔═══════╦═════╦══════╗           ┏━━━━━━━━━━━━━━━━━┿━┿━━━━━━━━━━━━━━━┓
 ┃ · · · · · ╮ · · ╵ ╵ · · · · · · · ┃          ║ Drive ║ Dir ║ Step ║           ┃ · · · · · ╮ · · ╵ ╵ · · · · · · · ┃
 ┃ · · · · · ╯ · · ╷ ╷ · · · · · · · ┃          ╠═══════╬═════╬══════╣           ┃ · · · · · ╯ · · ╷ ╷ · · · · · · · ┃
 ┗━━━━━━━━━━━━━━━━━┿━┿━━━━━━━━━━━━━━━┛          ║   0   ║   3 ║    5 ║           ┗━━━━━━━━━━━━━━━━━┿━┿━━━━━━━━━━━━━━━┛
 1                 └┬┘              33          ║   1   ║  11 ║   13 ║           1                 └┬┘              33
                    ⏚                           ║   2   ║  15 ║   19 ║                                                     ⏚
                                                ║   3   ║  21 ║   23 ║
                                                ║   4   ║  10 ║    8 ║
                                                ║   5   ║  16 ║   12 ║
                                                ║   6   ║  22 ║   18 ║
                                                ║   7   ║  26 ║   24 ║
                                                ╚═══════╩═════╩══════╝
                                                 Drive / GPIO mapping
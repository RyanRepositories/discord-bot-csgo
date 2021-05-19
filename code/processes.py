# Made in 2021 by Ryan C.
# This is the process files for main.py


# discord.py library
import discord

# other libraries
import json


# Grabs APIs from websites, parses them as JSON and writes them to a file
def api_grabber():

    import requests

    csgotrader_request = requests.get('https://prices.csgotrader.app/latest/prices_v6.json')
    print(f'CSGOtrader status code: {csgotrader_request.status_code}')
    csgotrader_data = csgotrader_request.json()
    with open('csgotrader_api.json', 'w') as api_data:
        json.dump(csgotrader_data, api_data)

    csgobackpack_request = requests.get('http://csgobackpack.net/api/GetItemsList/v2/?no_prices=False')
    print(f'CSGObackpack status code: {csgobackpack_request.status_code}')
    csgobackpack_data = csgobackpack_request.json()
    with open('csgobackpack_api.json', 'w') as api_data:
        json.dump(csgobackpack_data, api_data)

    conversion_rate_request = requests.get('https://api.exchangeratesapi.io/latest?base=USD')
    print(f'Conversion API status code: {conversion_rate_request.status_code}')
    conversion_rate_data = conversion_rate_request.json()
    with open('conversion_rate_api.json', 'w') as api_data:
        json.dump(conversion_rate_data, api_data)


def custom_help_output(command):

    if command == None:
        description = 'Welcome to the help command! ' + 'Here is the list of the commands:'
    else:
        description = f'Description and usage of the {command} command below:'

    # Output to Discord
    embed = discord.Embed(
            title = 'Help',
            description = description,
            colour = discord.Colour.blue()
        )

    embed.set_footer(text='Invite your friends to support the community!')
    embed.set_author(name='CSGO Market Bot',
                     icon_url='https://cdn.discordapp.com/avatars/819417852587016252/ac02c1d99e38546527659ff3dbb9acc0.png'
                    )

    if command is None:
        embed.add_field(name='Commands on this server:',
                value= 'help, price',
                inline=False
                       )
    elif command == "price":
        price_command = ["**Command description:** \n",
                        "Displays the item's price history, type of investment",
                        " and % increase relative to 24hr. Note that prices",
                        " are averaged across the named time period. \n\n",
                        "**Usage: ** \n",
                        '<"skin name"> (without the <>) is the full item name',
                        ' including the wear. Make sure to put brackets around',
                        ' the full name. Remember to use "★" on knife names if',
                        ' it applies. Example: "Glock-18 | Sand Dune', 
                        ' (Battle-Scarred)". \n\n',
                        '<currency> (without the <>) is the currency'
                        ' you want to use, if left blank it defaults to USD.'
                        ]

        embed.add_field(name='$price <"skin name"> <currency> ',
                value=(''.join(price_command)),
                inline=False
                      )

    return embed


# Process for $price "skin_name" conversion_rate
def price_output(skin_name, conversion_rate):

    # Check if skin_name == None
    if skin_name is None:
        embed = custom_help_output(command="price")
    else:
        # Imports API data into the function
        with open('csgotrader_api.json') as csgotrader_api_data:
            csgotrader_data = json.load(csgotrader_api_data)
        with open('csgobackpack_api.json') as csgobackpack_api_data:
            csgobackpack_data = json.load(csgobackpack_api_data)
        with open('conversion_rate_api.json') as conversion_rate_api_data:
            conversion_rate_data = json.load(conversion_rate_api_data)

        # Where the conversion rates are, defaulting to USD with empty param
        if conversion_rate is None:
            conversion_rate = "USD"
            exchange_rate = 1
        else:
            exchange_rate = float(conversion_rate_data["rates"][conversion_rate])

        # Prices with conversion rates factored in
        price_24h = round(exchange_rate * float(csgotrader_data[skin_name]["steam"]["last_24h"]), 2)
        price_7d = round(exchange_rate * float(csgotrader_data[skin_name]["steam"]["last_7d"]), 2)
        price_30d = round(exchange_rate * float(csgotrader_data[skin_name]["steam"]["last_30d"]), 2)
        price_90d = round(exchange_rate * float(csgotrader_data[skin_name]["steam"]["last_90d"]), 2)

        # Percentage rise relative to "last_24h"
        percentage_rise_90d = round(100 * price_24h / price_90d, 2)
        percentage_rise_30d = round(100 * price_24h / price_30d, 2)
        percentage_rise_7d = round(100 * price_24h / price_7d, 2)

        # Pulls the requested item's icon via steam image link
        icon_url = 'https://community.cloudflare.steamstatic.com/economy/image/' + csgobackpack_data["items_list"][skin_name]["icon_url"]

        # Decides what the link address is
        item_url_no_spaces = skin_name.replace(" ", "%20")
        steam_link_url = 'https://steamcommunity.com/market/listings/730/' + item_url_no_spaces

        # Decides what is the investment length
        if percentage_rise_90d > 100:
            investment_length = 'Long-term'
        else:
            investment_length = 'Not an ideal investment'
        if percentage_rise_30d > 115:
            investment_length = 'Medium'
        if percentage_rise_7d > 115:
            investment_length = 'Short'

        # Colour embed
        colour = csgobackpack_data["items_list"][skin_name]["rarity_color"]

        red = int("0x" + colour[:-4], 16)
        green = int("0x" + colour[2:-2], 16)
        blue = int("0x" + colour[4:], 16)

        # Output to Discord
        embed = discord.Embed(
                title = 'Requested Item:',
                description = skin_name,
                colour = discord.Colour.from_rgb(red, green, blue)
            )

        embed.set_footer(text='Invite your friends to support the community!')
        embed.set_thumbnail(url=icon_url)
        embed.set_author(name='CSGO Market Bot',
                        icon_url='https://cdn.discordapp.com/avatars/819417852587016252/ac02c1d99e38546527659ff3dbb9acc0.png'
                        )

        embed.add_field(name='Last 90 days',
                        value=(f'${price_90d} {conversion_rate} \n({percentage_rise_90d}%)'),
                        inline=True
                    )
        embed.add_field(name='Last 30 days',
                        value=(f'${price_30d} {conversion_rate} \n({percentage_rise_30d}%)'),
                        inline=True
                    )
        embed.add_field(name='Last 7 days',
                        value=(f'${price_7d} {conversion_rate} \n({percentage_rise_7d}%)'),
                        inline=True
                    )
        embed.add_field(name='Last 24 hours',
                        value=(f'${price_24h} {conversion_rate}'),
                        inline=True
                    )
        embed.add_field(name='Steam Link:',
                        value=(f'[Click here!]({steam_link_url})'),
                        inline=True
                    )
        embed.add_field(name='Short/Medium/Long-term investment?',
                        value=f'{investment_length}',
                        inline=False
                    )

    return embed


def error_message():

    # Output to Discord
    embed = discord.Embed(
                title = 'Error',
                description = 'You may be entering a wrong command, or missing an argument. Try `$help` to see the proper command usage',
                colour = discord.Colour.blue()
            )

    embed.set_footer(text='Invite your friends to support the community!')
    embed.set_author(name='CSGO Market Bot',
                    icon_url='https://cdn.discordapp.com/avatars/819417852587016252/ac02c1d99e38546527659ff3dbb9acc0.png'
                    )

    return embed

import requests
import simplejson as json
import time
import color
from color import out_color
import sys

api = ''


#api = raw_input('API : ')

starting_amount = int(input('Enter Starting Bet in Shatoshi : ' )) 
    

winchance = float(input('Enter Win Chance(0.01-99.98) : '))
condition = raw_input('Roll over(O) or roll under (U) : ')
on_loss_multiplier = float(input('On Loss Multiplier : '))
amount = starting_amount
bets_counter = 1


total_wins = 0
total_loses = 0



try:
    while True:
            
        
        #Primedice Settings(URL, Payload and Headers)
        url = 'http://api.primedice.com/api/bet?api_key=' + api
        payload = {'amount':amount,'target':winchance,'condition':condition}
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        #Makes the request to primedice
            
        r = requests.post(url, data=payload, headers=headers)

        #Passes the json content into response
        response = json.loads(r.text)

        bets_counter += 1

        bets_counter_print = 'Bet number : ' + str(bets_counter) + ' | '
        #Assigns some values into variables
        bet_result = response['bet']['win']
        bet_amount = 'Amount : ' + str(response['bet']['amount']) + ' | '
        bet_profit = 'Profit : ' + str(response['bet']['profit']) + ' | '
        bet_multiplier = response['bet']['multiplier']
        bet_condition = response['bet']['condition']
        bet_target = 'Target : ' + str(response['bet']['target']) + ' | '

        
        total_bets = total_wins + total_loses
        
        total_wagered = response['user']['wagered']
        conv_tot_wagered = total_wagered * float(0.00000001)
        printable_wagered = 'Wagered : ' + str(conv_tot_wagered) + '  |  '
        #Checks for loss
        result_counter = 0

        #Handles the loss result by multiplying the bet * 100
        if bet_result == False:
            result_counter = 1
            if result_counter == 1:
                amount = amount * on_loss_multiplier
        else:
            result_counter = 0
            amount = starting_amount
            
        #Checks for the result either win or loss
        if bet_result == True:
            result = 'Result: Win | '
        else:
            result = 'Result: Loss | '


        #Checks for the condition(Under or Over)
        if bet_condition == 'U' :
            bet_cond_value = 'Roll : Under | '
        else:
            bet_cond_value = 'Roll : Over | '

        #Variable with information to be printed
        printable = bets_counter_print + bet_cond_value + bet_target + bet_amount + bet_profit + result + printable_wagered

        #Prints info about the bet
        if bet_result == False:
            total_loses += 1
            print('\n' + out_color('red', printable))
        elif bet_result == True:
            total_wins += 1
            print('\n' + out_color('green', printable))
            
        #Time delay to slow down requests
        time.sleep(0.3)
        
except KeyboardInterrupt:
    print('\n')
    print('Wins : ' + out_color('green', str(total_wins)) + '  |  ' + 'Loses : ' + out_color('red', str(total_loses)) + '  |  Total Bets : ' + str(total_bets)) 
    pass


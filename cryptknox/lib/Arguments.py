class Arguments:
    def __init__(self,args):
        self.command = args[0] if args else None
        self.options = []
        self.optionValues = {}
        self.args = args[1:]


        i=0
        while i < len(self.args):
            arg = self.args[i]
            if arg.startswith('-'):
                self.options.append(arg)
                if i+1 < len(self.args) and not self.args[i+1].startswith('-'):
                    self.optionValues[arg] = self.args[i+1]
                    i+=1
            i+=1

        print(self.command)
        print(self.options)
        print(self.optionValues)
        print(self.args)
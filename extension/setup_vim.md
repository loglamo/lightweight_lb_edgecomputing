# Basic setups for Vim's interface
            $touch ~/.vimrc    //make hidden config vim file
            $vim ~/.vimrc      //to edit this config file 
            $mkdir -p ~/.vim ~/.vim/autoload ~/.vim/backup ~/.vim/colors ~/.vim/plugged    //create folders
            
1. There are a lot of plugins for Vim. Vim plugin managers should be used for managing all plugins. Some of the most popular ones are[1](https://linuxhandbook.com/install-vim-plugins/):
   - [vim-plug](https://github.com/junegunn/vim-plug?ref=linuxhandbook.com)
   - [VAM](https://github.com/MarcWeber/vim-addon-manager?ref=linuxhandbook.com)
   - [Vundle](https://github.com/VundleVim/Vundle.vim?ref=linuxhandbook.com)
   - [vim-pathogen](https://github.com/tpope/vim-pathogen?ref=linuxhandbook.com)
   
 ## The following steps setting Vim with vim-plug
 1. Install vim-plug:
       
             $curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim  //install vim-plug
             
 2. To add a plugin, use following code snippet in the vim config file ~/.vimrc:

              call plug#begin()
              
              Plug 'name_of_plugin'
              
              call plug#end()
              
 3. After editing vimrc file, save the file with:

               :source % 
               
 4. Start installing plugins with:
  
               :PlugInstall       //plugins declared in vimrc file will be installed 
              
 5. One of my setup for vim in 'vimrc'file in this repo, you can refer and use it
 

Title: Модификации Ведьмак 2
Date: 2016-08-26 20:09
Tags: witcher2
Category: Private
Author: Swasher
Status: draft

### Команды

Распаковать base_scripts.dzip в папку base_scripts

    Gibbed.RED.Unpack.exe base_scripts.dzip base_scripts

Упаковать папку base_scripts

    Gibbed.RED.Pack.exe base_scripts.dzip base_scripts

### Disable minimap rotation

in `base_scripts/game/gui/guihud.ws`

add line 518:

    cameraRot.Yaw = 180.0;
    
для Главы 2 и далее изменить на 

    cameraRot.Yaw = 0;
    
### Disble dark item visual effects

Find these lines

    SetDarkWeaponAddVitality( true );
    if(!thePlayer.IsDarkEffect())
    {
    if ( !thePlayer.IsNotGeralt() ) theCamera.PlayEffect('dark_difficulty');
    SetDarkEffect( true );
    }

Comment them out like this:

    SetDarkWeaponAddVitality( true );
    //if(!thePlayer.IsDarkEffect())
    //{
    // if ( !thePlayer.IsNotGeralt() ) theCamera.PlayEffect('dark_difficulty');
    // SetDarkEffect( true );
    //}

Это для серебрянного меча, чуть ниже то же самое для стального.

### Add 2 talent per level

in `base_scripts/game/player/player.ws` about line 4200

    // EXPERIENCE AND TALENT POINTS
    function ResetLevel()
    {
    level = 0;
    }
    // Levelup
    function SetLevelUp()
    {	
    var levelname : name;
    var talents : int;
    
    if (level < 35)
    {
    level = level + 1;
    
    talents = GetTalentPoints();
    SetTalentPoints( talents + 1 ); <----------------------------- Change the 1 to a 2.
    
    levelname = StringToName("Level" + level);
    GetCharacterStats().AddAbility( levelname );
    theSound.PlaySound("gui/other/levelup";
    theHud.m_hud.NotifyLevelUp( level );
    thePlayer.SendStatsToGui();
    
    }

